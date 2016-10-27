# ======================================================================== #
#
#       smoothingFilter.py
#       Jamieson Brynes
#       10/21/2016
#
#       This class contains the various smoothing functions for the smoothing
#       stage.
#
# ========================================================================= #


from src.infra.workerThread import WorkerThread
from src.infra.queue import Queue
from src.infra.simpleDataStructure import Sds
import src.utils as utils


class SmoothingFilter(WorkerThread):

    def centeredMovingAvg(self):
        while self.active:
            if not self.inputQueue.isEmpty():

                # Get next data point
                dp = self.inputQueue.dequeue()

                # Special handling for end data stream
                if dp == 'end':
                    self.outputQueue.enqueue(dp)
                    self.completed = True
                    self.active = False
                    return

                self.data.append(dp)
                self.window.enqueue(dp)

                if len(self.window) == self.windowSize:
                    # Do smoothing action and pop.
                    ssum = 0
                    for i in range(len(self.window)):
                        ssum += self.window[i].mag
                    # Average of all points in the window
                    new_dp = Sds(self.window[int(self.windowSize / 2)].time, ssum / self.windowSize)
                    self.outputQueue.enqueue(new_dp)
                    self.window.dequeue()

    # Constructor for the window
    # @args:
    #   1. params - dictionary containing relevant parameter
    #       a. 'window_size' - size of the window. NOTE: Should be odd.
    #   2. inputData - queue object containing the pre-processed data
    #   3. smoothData - queue object containing the smoothed data
    def __init__(self, params, inputData, dataList, smoothData):

        super(SmoothingFilter, self).__init__()

        # Internal references to queues
        self.inputQueue = inputData
        self.outputQueue = smoothData
        self.data = dataList

        # Params unpacking
        self.windowSize = params['window_size']
        self.typ = params['type']

        # Internal buffer
        self.window = Queue()

        # Set correct target
        if self.typ == 'center_moving_avg':
            self.target = self.centeredMovingAvg
        else:
            self.target = self.centeredMovingAvg





