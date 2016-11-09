# ======================================================================== #
#
#       postProcessing.py
#       Jamieson Brynes
#       10/22/2016
#
#       This class contains the implementation of the post-processing stage.
#
# ========================================================================= #

from src.infra.queue import Queue
from src.infra.workerThread import WorkerThread


class WpdPostProcessor(WorkerThread):

    # Worker function for the post processing
    def postProcess(self):
        while self.active:
            if not self.inputQueue.isEmpty():

                # Get next data point
                dp = self.inputQueue.dequeue()

                # Special case handling for last data point
                if dp == 'end':
                    self.completed = True
                    self.active = False
                    pop = self.queue.dequeue()
                    self.outputList.append(pop)
                    return

                # If we have less than 2 points in the queue, just enqueue
                if len(self.queue) < 1:
                    self.queue.enqueue(dp)
                else:
                    # If the time difference exceeds the threshold, pop the old point
                    if (dp.time - self.queue[0].time) > self.timeThreshold:
                        pop = self.queue.dequeue()
                        self.outputList.append(pop)
                        self.queue.enqueue(dp)
                    # Else only keep the maximum value point
                    else:
                        if dp.mag >= self.queue[0].mag:
                            pop = self.queue.dequeue()
                            self.queue.enqueue(dp)

    # Constructor
    # @args:
    #   1. params - dictionary to contain parameters
    #       a. 'time_threshold' - time threshold for eliminating peaks
    #   2. inputPeaks - input data queue with potential peaks
    #   3. confirmedPeaks - output data list for confirmed peaks
    def __init__(self, params, inputPeaks, confirmedPeaks):

        super(WpdPostProcessor, self).__init__()
        self.target = self.postProcess

        # Internal references
        self.inputQueue = inputPeaks
        self.outputList = confirmedPeaks

        # Param unpacking
        self.timeThreshold = params['time_threshold']

        # Internal queue
        self.queue = Queue()
