# ======================================================================== #
#
#       preProcessing.py
#       Jamieson Brynes
#       10/22/2016
#
#       This class contains the pre processing element for the data points.
#       It will compute their magnitude, scale the time, and interpolate
#       between points
#
#
# ======================================================================== #

import time
import math

import src.utils as utils
from src.infra.queue import Queue
from src.constants import Constants
from src.infra.workerThread import WorkerThread


class WpdPreProcessor(WorkerThread):

    def preProcess(self):
        while self.active:
            if not self.inputQueue.isEmpty():
                # Pop oldest point on the queue
                ds = self.inputQueue.dequeue()

                # Special handling for the 'end' of the data stream
                if ds == 'end':
                    self.dataQueue.enqueue('end')
                    self.completed = True
                    self.active = False
                    return

                # Handling for the first data point received
                if self.startTime is None:
                    self.startTime = ds.getTime()

                # Scale time and compute magnitude
                ds.scaleTime(self.startTime, self.ts_factor)
                ds.computeMagnitude()

                # Add the datapoint to the working window and the list of data
                self.window.enqueue(ds)
                self.dataList.append(ds)

                # If we have more than 1 point in the queue
                if self.window.size() >= 2:

                    # Timestamps
                    time1 = self.window[0].getTime()
                    time2 = self.window[1].getTime()

                    # Check how many interpolation points COULD lie in between the timestamps
                    for i in range(math.ceil((time2 - time1) / self.interp_ts)):
                        interp_time = self.interpolation_count * self.interp_ts
                        # If the interpolated time lies in this range, create the new data point and add it
                        if time1 <= interp_time < time2:
                            sds = utils.linearInterp(self.window[0], self.window[1], interp_time)
                            self.dataQueue.enqueue(sds)
                            self.interpolation_count += 1

                    # Pop the most recent element
                    self.window.dequeue()
            else:
                time.sleep(Constants.THREAD_SLEEP_PERIOD)

    # Constructor for object.
    # @args:
    #   1. params - a dictionary containing parameters for the preprocessor
    #       a. 'inter_ts' : interpolation time scale in ms
    #       b. 'ts_factor' : time scale factor (i.e. if you want to go from ns to ms, this should be 1,000,000)
    #   2. inputQueue - the queue from the inputPipe, raw data
    #   3. dataList - a list of data to permanently store the unaltered data
    #   4. dataQuee - a queue for the preprocessed data to be put into
    # Worker function for thread
    def __init__(self, params, inputQueue, dataList, dataQueue):

        super(WpdPreProcessor, self).__init__()
        self.target = self.preProcess

        # Internal references to data structures
        self.inputQueue = inputQueue
        self.dataList = dataList
        self.dataQueue = dataQueue

        # Params unpacking
        self.interp_ts = params['inter_ts']
        self.ts_factor = params['ts_factor']

        # Internal buffer
        self.window = Queue()

        # Data processing parameters
        self.startTime = None
        self.interpolation_count = 0

