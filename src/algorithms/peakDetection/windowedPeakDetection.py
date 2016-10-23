#========================================================================#
#
#       windowedPeakDetection.py
#       Jamieson Brynes
#       10/22/2016
#
#       This class contains the implementation of the windowed peak
#       detection algorithm. Agnostic to smoothing window type and
#       peak 'score' function calculator.
#
#========================================================================#

from src.constants import constants

from src.infra.queue import Queue

from src.algorithms.peakDetection.peakDetector import PeakDetector
from src.algorithm.peakDetection.postProcessing import WpdPostProcessor
from src.algorithm.peakDetection.preProcessing import WpdPreProcessor

class Wpd :

    #Constructor for the object.
    # @args :
    #   1. queue - the input data stream queue from inputPipe
    #   2. preProcessingParams - parameters for the preprocessor, see preProcessing.py for docs
    #   3. windowType - type of windowing for the smoothing process. See constants.py for list.
    #   4. windowParams - parameters for the preprocessor, see relevant windowing function for docs.
    #   5. peakFuncType - type of peak scoring function. See constants.py for the list
    #   6. peakFuncParams - parameters for the peak scoring function, see relevant scoring function for docs.
    #   7. peakDetectorParams - parameters for the peak detector, see peakDetector.py for docs.
    #   8. postProcessingParams - parameters for post processing, see postProcessing.py for docs.
    def __init__(self, queue, preProcessingParams, windowType, windowParams, peakFuncType, peakFuncParams, peakDetectorParams, postProcessingParams) :
        #Data about found peaks.
        self.confirmedPeaks = []

        #Internal queues for data flow
        self.inputQueue = queue
        self.dataQueue = Queue()
        self.smoothedDataQueue = Queue()
        self.peakScores = Queue()
        self.peaks = Queue()

        #Internal list for permanent data
        self.data = []
        self.smoothedData = []
        self.peakyData = []

        #Internal 'worker threads' in the form of objects
        self.preProcessing = WpdPreProcessor(preProcessingParams, self.inputQueue, self.data, self.dataQueue)
        self.window = Constants.SMOOTHING_WINDOWS[windowType](windowParams, self.dataQueue, self.smoothedDataQueue)
        self.peakScorer = Constants.PEAKY_FUNCTIONS[peakFuncType](peakFuncParams, self.smoothedDataQueue, self.smoothedData, self.peakScores)
        self.peakDetection = PeakDetector(PeakDetectorParams, self.peakScores, self.peakyData, self.peaks, )
        self.postProcessing = WpdPostProcessor(postProcessingParams, self.peaks, self.confirmedPeaks)


    def start(self) :
        #Start preprocessing thread
        self.preProcessing.start()
        #Start window smoothing thread
        self.window.start()
        #Start peak function thread
        self.peakScorer.start()
        #Start peak detection thread
        self.peakDetection.start()
        #Start data post processing thread
        self.postProcessing.start()

    def stop(self) :

        self.preProcessing.stop()
        self.window.stop()
        self.peakScorer.stop()
        self.peakDetection.stop()
        self.postProcessing.stop()

    def isDone(self) :
        return self.preProcessing.isDone() && self.window.isDone() && self.peakScorer.isDone() && self.peakDetection.isDone() && self.postProcessing.isDone()

    def isRunning(self) :
        return self.preProcessing.isRunning() or self.window.isRunning() or self.peakScorer.isRunning() or self.peakDetection.isRunning() or self.postProcessing.isRunning() :

    #Getters
    def getRawData(self) :
        return self.data


    def getSmoothedData(self) :
        return self.smoothedData


    def getPeakyData(self) :
        return self.peakyData


    def getPeaks(self) :
        return self.confirmedPeaks

    def getSteps(self) :
        return len(self.confirmedPeaks)
