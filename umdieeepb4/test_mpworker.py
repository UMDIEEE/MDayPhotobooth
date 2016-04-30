import os
import mpworker

status_map = {
                0: "IMPROC_NOT_STARTED",
                1: "IMPROC_RUNNING",
                2: "IMPROC_FAILED",
                3: "IMPROC_SUCCESS"
            }

job_map = {}

def callback(job_id, status):
    print("%s: %s" % (job_map[job_id], status_map[status]))

imp = mpworker.ImageProcessing(callback = callback)

for f in os.listdir('assets/frames'):
    orig_path = os.path.join('assets/frames', f)
    if os.path.isfile(orig_path):
        new_path = "tmp/" + f
        print("%s -> %s" % (orig_path, new_path))
        job_map[imp.add_job(["shrink43Image", orig_path, new_path])] = orig_path

imp.finish_jobs()
imp.stop()
