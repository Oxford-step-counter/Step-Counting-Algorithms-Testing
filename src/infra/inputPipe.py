#========================================================================#
#
#       inputPipe.py
#       Jamieson Brynes
#       10/21/2016
#
#       This class is designed to simulate the real time collection of data
#       points. It will deposit the data into a queue at a fixed sampling
#       rate.
#
#=========================================================================#

from threading import Thread
import time
from src.constants import Constants
import src.utils as utils


class InputPipe:

    # Constructor
    # @args :
    #   1. filepath - path to the input accelerometer data to parse
    #   2. queue - the Queue object to add the data to.
    def __init__(self, filepath, queue):
        self.filepath = filepath
        self.queue = queue

        self.thread = None

    # Start the piping operation
    def start(self):

        try:
            self.thread = Thread(target = self.pipeInput, args = ())
            self.thread.daemon = True
            self.thread.start()
        except:
            print('Error: Cannot start piping thread')

    # Check if the piping operation is still running
    def isRunning(self):

        if hasattr(self, 'thread'):
            return self.thread.isAlive()
        else:
            return False

    # Stop the piping operation
    def stop(self):

        if self.thread:
            self.thread.stop()

    # Worker function for the thread
    def pipeInput(self):

        data = utils.loadAccelCsv(self.filepath)

        for datapoint in data:
            self.queue.enqueue(datapoint)
            # time.sleep(Constants.SAMPLE_PERIOD)

        # Add an 'end' signal to the pipe to indicate the end of the data stream
        self.queue.enqueue('end')
