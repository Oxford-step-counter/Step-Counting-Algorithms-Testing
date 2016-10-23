#========================================================================#
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
#========================================================================#

from threading import Thread
import time
import math

import src.utils as utils
from src.infra.queue import Queue
from src.constants import Constants

class WpdPreProcessor :


    #Constructor for object.
    # @args:
    #   1. params - a dictionary containing parameters for the preprocessor
    #       a. 'inter_ts' : interpolation time scale in ms
    #       b. 'ts_factor' : time scale factor (i.e. if you want to go from ns to ms, this should be 1,000,000)
    #   2. inputQueue - the queue from the inputPipe, raw data
    #   3. dataList - a list of data to permanently store the unaltered data
    #   4. dataQuee - a queue for the preprocessed data to be put into
    def __init__(self, params, inputQueue, dataList, dataQueue) :

        #Thead variables
        self.thread = None
        self.active = False
        self.completed = False

        #Internal references to data structures
        self.inputQueue = inputQueue
        self.dataList = dataList
        self.dataQueue = dataQueue

        #Params unpacking
        self.interp_ts = params['inter_ts']
        self.ts_factor = params['ts_factor']

        #Internal buffer
        self.window = Queue()

        #Data processing parameters
        self.startTime = None
        self.interpolation_count = 0


    def start(self) :
        self.active = True
        self.thread = Thread(target = self.preProcess, args=())
        self.thread.daemon = True
        self.thread.start()
        utils.threadLog('Preprocessing thread started')


    def isRunning(self) :

        #If the program is in 'active' mode AND the thread is actually still running.
        return self.active and True if (self.thread and self.thread.isAlive()) else False

    def isDone(self) :

        return self.completed


    def stop(self) :

        utils.threadLog('Preprocessing thread stopped.')
        self.active = False


    def preProcess(self) :

        while self.active :
            if not self.inputQueue.isEmpty() :
                #Pop oldest point on the queue and computeMagnitude
                ds = self.inputQueue.dequeue()

                #Special handling for the 'end' of the data stream
                if ds == 'end' :
                    self.dataQueue.enqueue('end')
                    self.completed = True
                    return

                ds.computeMagnitude()
                #Handling for the first data point received
                if self.startTime == None :
                    self.startTime = ds.getTime()

                #Scale time
                ds.scaleTime(self.startTime, self.ts_factor)

                self.window.enqueue(ds)
                self.dataList.append(ds)

                if self.window.size() >= 2 :
                    #Process data and pop.

                    time1 = self.window[0].getTime()
                    time2 = self.window[1].getTime()


                    for i in range(math.ceil((time2 - time1) / self.interp_ts)) :
                        interp_time = (self.interpolation_count) * self.interp_ts
                        if time1 <= interp_time and time2 > interp_time :
                            sds = utils.linearInterp(self.window[0], self.window[1], interp_time)
                            self.dataQueue.enqueue(sds)
                            self.interpolation_count += 1

                    #Pop the most recent element
                    self.window.dequeue()

            time.sleep(Constants.THREAD_SLEEP_PERIOD)
