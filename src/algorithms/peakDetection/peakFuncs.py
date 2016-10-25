
from threading import Thread

from src.infra.queue import Queue
from src.infra.simpleDataStructure import Sds

class MaxDiff:

    # Constructor for the object
    # @args:
    #   1. params - dictionary containing relevant parameters
    #       a. 'window_size' - size of the window
    #   2. smoothData - queue containing smoothed data
    #   3. smoothDataList - list containing smoothed data
    #   4. peakScores - queue containing peak scores data
    def __init__(self, params, smoothData, smoothDataList, peakScores):

        # Thread variables
        self.thread = None
        self.active = False
        self.completed = False

        # Internal references for smooth data
        self.inputQueue = smoothData
        self.data = smoothDataList
        self.outputQueue = peakScores

        # Internal window
        self.window = Queue()

        # Parameter unpacking
        self.windowSize = params['window_size']

    def start(self):
        # Start 'worker thread'
        self.active = True
        self.thread = Thread(target=self.maxDiff, args=())
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.active = False

    def isRunning(self):
        return self.active and (True if (self.thread is not None and self.thread.isAlive) else False)

    def isDone(self):
        return self.completed

    def maxDiff(self):
        while self.active:
            if not self.inputQueue.isEmpty():

                # Get next data point
                dp = self.inputQueue.dequeue()

                # Special case handling for end data point.
                if dp == 'end':
                    self.completed = True
                    self.active = False
                    self.outputQueue.enqueue('end')
                    return

                # Add data point to list and queue
                self.data.append(dp)
                self.window.enqueue(dp)

                # Once we reach the window size, do some processing!
                if len(self.window) == self.windowSize:

                    # Calculate peak score
                    midPoint = int(self.windowSize / 2)
                    maxDiffLeft = -100
                    maxDiffRight = -100

                    # Find max difference on left
                    for i in range(0, midPoint):
                        value = self.window[midPoint].mag - self.window[i].mag
                        if value > maxDiffLeft:
                            maxDiffLeft = value

                    # Find max difference on right
                    for i in range(midPoint + 1, len(self.window)):
                        value = self.window[midPoint].mag - self.window[i].mag
                        if value > maxDiffRight:
                            maxDiffRight = value

                    # Calculate peak score and create a new point
                    avg = (maxDiffRight + maxDiffLeft) / 2
                    new_dp = Sds(self.window[midPoint].time, avg, self.window[midPoint].mag)
                    self.outputQueue.enqueue(new_dp)
                    self.window.dequeue()
