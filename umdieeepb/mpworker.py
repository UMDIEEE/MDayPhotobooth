import multiprocessing
import queue
import subprocess
import time

NUM_CPUS = 3

# Global job status constants
IMPROC_NOT_STARTED = 0
IMPROC_RUNNING = 1
IMPROC_FAILED = 2
IMPROC_SUCCESS = 3

# Debug flag
IMPROC_DEBUG = False

def dprint(text):
    if IMPROC_DEBUG:
        print(text)

def file_rename(oldfn, suffix):
    imgarr = img_name.split('.')
    basename = ".".join(imgarr[:-1])
    ext = imgarr[-1]
    newfn = basename + "_new" + "." + ext

class ImageProcessing:
    def __init__(self, callback = None):
        self.cur_job_id = -1
        self.jobs = []
        self.jobs_status = []
        
        self.task_queue = multiprocessing.Queue()
        self.result_queue = multiprocessing.Queue()
        
        self.callback = callback
        
        self.mphelper = ImageProcessingDistributerMP(self.task_queue, self.result_queue)
        
        dprint("[ImageProcessing] MPHelper started.")
    
    def start(self):
        self.mphelper.start()
    
    # Input task format:
    # [ op_type, args.... (input, output, etc.) ]
    # Return job ID
    def add_job(self, task):
        self.cur_job_id += 1
        self.jobs.append([self.cur_job_id] + task)
        self.jobs_status.append(IMPROC_NOT_STARTED)
        self.task_queue.put(self.jobs[self.cur_job_id])
        
        dprint("[ImageProcessing.add_job] Sending job to MPHelper: %s (job %i)" % (str(task), self.cur_job_id))
        
        return self.cur_job_id
    
    def check_job(self, job_id):
        return self.jobs_status[job_id]
    
    def process_jobs(self):
        while 1:
            # Fetch results in the result queue
            try:
                # Result format:
                # [ job_id, status ]
                next_result = self.result_queue.get(False)
                
                # Process it:
                self.jobs_status[next_result[0]] = next_result[1]
                
                # Run callback if specified...
                if self.callback:
                    self.callback(next_result[0], next_result[1])
                
                dprint("[ImageProcessing.process_jobs] Got result: %s" % (str(next_result)))
            except queue.Empty:
                dprint("[ImageProcessing.process_jobs] No more results, returning.")
                break
            
            # Wait a bit before looping back
            time.sleep(0.1)
    
    # Block until all current jobs are finished.
    def finish_jobs(self):
        while (self.jobs_status.count(IMPROC_NOT_STARTED) + self.jobs_status.count(IMPROC_RUNNING)) > 0:
            self.process_jobs()
            time.sleep(0.1)
    
    # Block until all current jobs are finished, and then reset.
    def finish_jobs_and_reset(self):
        self.finish_jobs()
        self.reset()
    
    def reset(self):
        self.cur_job_id = -1
        self.jobs = []
        self.jobs_status = []
    
    def stop(self):
        dprint("[ImageProcessing.stop] Stopping... (sending poison pill)")
        self.task_queue.put(None)
        dprint("[ImageProcessing.stop] Waiting for stop to complete.")
        self.mphelper.join()

class ImageProcessingDistributerMP(multiprocessing.Process):
    # task_queue - tasks queue
    # result_queue - notification queue to send to
    #     [job_id, status]
    #         job_id - job ID, incrementing.
    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
        
        self.num_procs = 0
        
        self.tasks = []
        self.running_mp_procs = []
        
        self.stopnow = False
        
        dprint("[ImageProcessingDistributerMP.__init__] Initialized.")
    
    def run(self):
        dprint("[ImageProcessingDistributerMP.run] Starting distributer loop.")
        while 1:
            # Fetch tasks in the task queue
            while 1:
                try:
                    # Task format:
                    # [ job_id, op_type, args... ]
                    next_task = self.task_queue.get(False)
                    
                    # Poison pill - exit this if we get this!
                    if next_task == None:
                        self.stopnow = True
                        break
                    
                    # Otherwise, process and distribute it.
                    self.tasks.append(list(next_task))
                    
                    dprint("[ImageProcessingDistributerMP.run] Task received: %s" % str(next_task))
                except queue.Empty:
                    dprint("[ImageProcessingDistributerMP.run] No more tasks, moving on.")
                    break
                
                # Sleep a bit
                time.sleep(0.1)
            
            # Process current tasks
            for mp_proc in self.running_mp_procs:
                if not mp_proc.is_alive():
                    dprint("[ImageProcessingDistributerMP.run] Found completed process, removing it.")
                    self.running_mp_procs.remove(mp_proc)
                    self.num_procs -= 1
                else:
                    # If we are stopping, terminate everything.
                    if self.stopnow:
                        dprint("[ImageProcessingDistributerMP.run] Ending process due to stop signal.")
                        mp_proc.terminate()
                        self.running_mp_procs.remove(mp_proc)
                        self.num_procs -= 1
            
            # Process new tasks, and add them if we have room
            # ONLY if we are still running, though!
            if (not self.stopnow) and (self.num_procs < NUM_CPUS):
                for new_task in self.tasks:
                    if self.num_procs >= NUM_CPUS:
                        dprint("[ImageProcessingDistributerMP.run] Out of CPUs, moving on.")
                        break
                    dprint("[ImageProcessingDistributerMP.run] Queueing task: %s" % str(new_task))
                    self.running_mp_procs.append(ImageProcessingWorkerMP(list(new_task), self.result_queue))
                    self.running_mp_procs[len(self.running_mp_procs) - 1].start()
                    self.num_procs += 1
                    self.tasks.remove(new_task)
            
            # Check if we need to exit
            if self.stopnow:
                dprint("[ImageProcessingDistributerMP.run] Got stop signal, exiting.")
                break
            
            dprint("[ImageProcessingDistributerMP.run] End of loop stats: %i/%i CPUs used, %i tasks left" % (self.num_procs, NUM_CPUS, len(self.tasks)))
            
            # Wait a bit, we just did a lot!
            time.sleep(0.1)
    

class ImageProcessingWorkerMP(multiprocessing.Process):
    # op_type (from task format above)
    # args - arguments to the function being called
    # result_queue - notification queue to send to
    def __init__(self, task, result_queue):
        multiprocessing.Process.__init__(self)
        self.task = task
        self.result_queue = result_queue
    
    def run(self):
        # Task format:
        # [ job_id, op_type, args... ]
        dprint("[ImageProcessingWorkerMP.run] Running task: %s" % (str(self.task)))
        if self.task[1] == "shrink43Image":
            self.proc_proc(self.shrink43Image, self.task[2:])
        elif self.task[1] == "frame_pic":
            self.proc_proc(self.frame_pic, self.task[2:])
        else:
            self.result_queue.put([self.task[0], IMPROC_FAILED])
    
    # proc_proc
    #     General function handler - run the function,
    #     handle signals
    def proc_proc(self, func, args):
        dprint("[ImageProcessingWorkerMP.proc_proc] Sending running signal for job ID %i." % (self.task[0]))
        
        # Send running signal
        self.result_queue.put([self.task[0], IMPROC_RUNNING])
        
        # Run the function
        ret = func(*args)
        
        # Send result signal
        if ret == 0:
            dprint("[ImageProcessingWorkerMP.proc_proc] Sending SUCCESS signal for job ID %i." % (self.task[0]))
            self.result_queue.put([self.task[0], IMPROC_SUCCESS])
        else:
            dprint("[ImageProcessingWorkerMP.proc_proc] Sending FAILED signal for job ID %i. (ret = %i)" % (self.task[0], ret))
            self.result_queue.put([self.task[0], IMPROC_FAILED])
    
    # run_proc
    #     subprocess running wrapper
    #     return the return code
    def run_proc(self, proc_arr):
        dprint("[ImageProcessingWorkerMP.run_proc] Running: %s" % (str(proc_arr)))
        s = subprocess.Popen(proc_arr)
        s.communicate()
        return s.returncode
    
    def shrink43Image(self, img_name, new_img_name):
        dprint("[ImageProcessingWorkerMP.shrink43Image] Shrinking to 177x236: %s -> %s" % (img_name, new_img_name))
        return self.run_proc(['convert', img_name, '-resize', '177x236', new_img_name])
    
    def frame_pic(self, img_name, frame_img_name, new_img_name):
        dprint("[ImageProcessingWorkerMP.frame_pic] Framing picture: %s + %s -> %s" % (img_name, frame_img_name, new_img_name))
        return self.run_proc(['composite', '-compose', 'atop', '-gravity', 'center', frame_img_name, img_name, new_img_name])
