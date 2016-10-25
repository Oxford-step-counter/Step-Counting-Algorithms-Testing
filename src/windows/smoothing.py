#========================================================================#
#
#       smoothing.py
#       Jamieson Brynes
#       10/21/2016
#
#       This class contains the various smoothing functions for the smoothing
#       stage.
#
#=========================================================================#

from src.infra.queue import Queue
from src.infra.simpleDataStructure import Sds
import src.utils as utils

from threading import Thread

class CenterMovingAvg:

    # Constructor for the window
    # @args:
    #   1. params - dictionary containing relevant parameter
    #       a. 'window_size' - size of the window. NOTE: Should be odd.
    #   2. inputData - queue object containing the pre-processed data
    #   3. smoothData - queue object containing the smoothed data
    def __init__(self, params, inputData, dataList, smoothData):

        # Thread variables
        self.thread = None
        self.active = False
        self.completed = False

        # Internal references to queues
        self.inputQueue = inputData
        self.outputQueue = smoothData
        self.data = dataList

        # Params unpacking
        self.windowSize = params['window_size']

        # Internal buffer
        self.window = Queue()

    def start(self):
        self.active = True
        self.thread = Thread(target=self.smooth, args=())
        self.thread.daemon = True
        self.thread.start()
        utils.threadLog('Started smoothing thread')

    def stop(self):
        utils.threadLog('Stopped smoothing thread')
        self.active = False

    def isRunning(self):
        return self.active and (True if self.thread is not None and self.thread.isAlive() else False)

    def isDone(self):
        return self.completed

    def smooth(self):
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




