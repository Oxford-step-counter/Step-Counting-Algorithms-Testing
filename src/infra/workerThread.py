
import src.utils as utils
from threading import Thread


class WorkerThread:

    def __init__(self):

        # Thread related variables
        self.thread = None
        self.active = False
        self.completed = False
        self.target = None
        self.args = ()

    # Start signal, create and kick off thread
    def start(self):
        self.active = True
        self.thread = Thread(target=self.target, args=self.args)
        self.thread.daemon = True
        self.thread.start()
        utils.threadLog('Pre-processing thread started')

    # Stop signal, end thread after current operation is done
    def stop(self):
        utils.threadLog('Pre-processing thread stopped.')
        self.active = False

    # Check if the thread is running
    def isRunning(self):
        # If the program is in 'active' mode AND the thread is actually still running.
        return self.active and (True if (self.thread and self.thread.isAlive()) else False)

    # Check if the pre-processing stage is finished
    def isDone(self):
        return self.completed