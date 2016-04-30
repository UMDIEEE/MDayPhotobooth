import threading
import queue

class StoppableThread():
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = False
        self.stopnow = False
        self.stop_queue = queue.Queue()
        self.thread = None
    
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.main, args=(self.stop_queue,))
        self.thread.start()
    
    def need_to_stop(self, stop_queue):
        try:
            s = stop_queue.get(False)
            if s:
                return True
            return False
        except queue.Empty:
            return False
    
    def stop(self):
        self.stop_queue.put(True)
        self.thread.join()
    

