# ======================================================================== #
#
#       windowedPeakDetection.py
#       Jamieson Brynes
#       10/22/2016
#
#       This class contains the implementation of the windowed peak
#       detection algorithm. Agnostic to smoothing window type and
#       peak 'score' function calculator.
#
# ======================================================================== #
from src import utils

from src.infra.inputPipe import InputPipe
from src.infra.queue import Queue

from src.algorithms.peakDetection.preProcessing import WpdPreProcessor
from src.algorithms.peakDetection.smoothingFilter import SmoothingFilter
from src.algorithms.peakDetection.peakFuncs import PeakScorer
from src.algorithms.peakDetection.peakDetector import PeakDetector
from src.algorithms.peakDetection.postProcessing import WpdPostProcessor



class Wpd:

    # Constructor for the object.
    # @args :
    #   1. filelocation - location of the accelerometer_test.csv and stepcounter.csv
    #   2. preProcessingParams - parameters for the preprocessor, see preProcessing.py for docs
    #   3. windowType - type of windowing for the smoothing process. See constants.py for list.
    #   4. windowParams - parameters for the preprocessor, see relevant windowing function for docs.
    #   5. peakFuncType - type of peak scoring function. See constants.py for the list
    #   6. peakFuncParams - parameters for the peak scoring function, see relevant scoring function for docs.
    #   7. peakDetectorParams - parameters for the peak detector, see peakDetector.py for docs.
    #   8. postProcessingParams - parameters for post processing, see postProcessing.py for docs.
    def __init__(self, filelocation, preProcessingParams, windowParams, peakFuncParams, peakDetectorParams, postProcessingParams):

        self.name = 'wpd'
        self.filelocation = filelocation

        # Internal queues for data flow
        self.inputQueue = Queue()
        self.dataQueue = Queue()
        self.smoothedDataQueue = Queue()
        self.peakScores = Queue()
        self.peaks = Queue()

        # Internal plottable lists for plottable data
        self.data = []
        self.preprocessData = []
        self.smoothedData = []
        self.peakScoreData = []
        self.peakData = []
        self.confirmedPeaks = []
        self.steps = []

        # Internal 'worker threads' in the form of objects
        self.pipe = InputPipe(self.filelocation, self.inputQueue)
        self.preProcessing = WpdPreProcessor(preProcessingParams, self.inputQueue, self.data, self.dataQueue)
        self.smoothingFilter = SmoothingFilter(windowParams, self.dataQueue, self.preprocessData, self.smoothedDataQueue)
        self.peakScorer = PeakScorer(peakFuncParams, self.smoothedDataQueue, self.smoothedData, self.peakScores)
        self.peakDetection = PeakDetector(peakDetectorParams, self.peakScores, self.peakScoreData, self.peaks, self.peakData)
        self.postProcessing = WpdPostProcessor(postProcessingParams, self.peaks, self.confirmedPeaks)

    # Start algorithm signal, kicks off all the worker threads for the various stages
    def start(self):

        self.pipe.start()
        self.preProcessing.start()
        self.smoothingFilter.start()
        self.peakScorer.start()
        self.peakDetection.start()
        self.postProcessing.start()

    # Stop algorithm signal, halts all the worker threads after the current operation
    def stop(self):

        self.pipe.start()
        self.preProcessing.stop()
        self.smoothingFilter.stop()
        self.peakScorer.stop()
        self.peakDetection.stop()
        self.postProcessing.stop()

    def getStatus(self):

        return 'Input Data: ' + str(len(self.inputQueue)) \
               + ' Pre-Processed Data: ' + str(len(self.dataQueue)) \
               + ' Smoothed Data: ' + str(len(self.smoothedDataQueue)) \
               + ' Peak Scores: ' + str(len(self.peakScores)) \
               + ' Peaks: ' + str(len(self.peaks)) \
               + ' Confirmed Peaks: ' + str(len(self.confirmedPeaks))

    def getCsvStatus(self):

        return str(len(self.inputQueue)) + ',' \
               + str(len(self.dataQueue)) + ',' \
               + str(len(self.smoothedDataQueue)) \
               + ',' + str(len(self.peakScores)) \
               + ',' + str(len(self.peaks)) \
               + ',' + str(len(self.confirmedPeaks))

    def compare(self):

        #timeData = {'scale': self.preProcessing.ts_factor, 'offset': self.preProcessing.startTime}
        #self.steps = utils.loadStepCsv(self.filelocation + 'stepcounter.csv', timeData)
        return [len(self.confirmedPeaks), 0]

    # Check if the algorithm is done
    def isDone(self):
        return self.preProcessing.isDone()and self.smoothingFilter.isDone() and self.peakScorer.isDone() and self.peakDetection.isDone() and self.postProcessing.isDone()

    # Check if the algorithm is still running
    def isRunning(self):
        return self.preProcessing.isRunning() or self.smoothingFilter.isRunning() or self.peakScorer.isRunning() or self.peakDetection.isRunning() or self.postProcessing.isRunning()

    # Getters

    def getData(self):
        return [self.data, self.preprocessData, self.smoothedData, self.peakScoreData, self.peakData, self.confirmedPeaks]

    def getName(self):
        return self.name

    def getSteps(self):
        return len(self.confirmedPeaks)
