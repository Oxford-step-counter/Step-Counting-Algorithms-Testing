# ======================================================================== #
#
#       peakDetector.py
#       Jamieson Brynes
#       10/22/2016
#
#       This class contains the implementation of the peak detection
#       algorithm. It uses a simple mean and standard deviation method
#       to find significant values of peak scores.
#
# ======================================================================== #

import math

from src.infra.simpleDataStructure import Sds
from src.infra.workerThread import WorkerThread


class PeakDetector(WorkerThread):

    # Worker function for peak detection.
    def peakDetect(self):
        while self.active:
            if not self.inputQueue.isEmpty():

                # Get next data point
                dp = self.inputQueue.dequeue()

                # Special handling for end case
                if dp == 'end':
                    self.active = False
                    self.completed = True
                    self.outputQueue.enqueue('end')
                    return

                # Add to data list
                self.data.append(dp)

                # Update statistics
                self.n += 1
                if self.n == 1:
                    # First data point
                    self.mean = dp.mag
                    self.std = 0
                elif self.n == 2:
                    # Second data point
                    o_mean = self.mean
                    self.mean = (dp.mag + self.mean) /2
                    self.std = math.sqrt((math.pow(dp.mag - self.mean, 2) + math.pow(o_mean - self.mean, 2)) / 2)
                else:
                    # Iteratively update mean and standard deviation
                    self.std = math.sqrt(((self.n - 2) * math.pow(self.std, 2) / (self.n - 1)) + math.pow(dp.mag - self.mean, 2) / self.n)
                    self.mean = (dp.mag + (self.n - 1) * self.mean) / self.n
                if self.n > 15:
                    # Check if we are above the threshold
                    if (dp.mag - self.mean) > self.std * self.threshold:
                        # Declare this a peak
                        self.outputQueue.enqueue(Sds(dp.time, dp.oldMag))
                        self.dataout.append(Sds(dp.time, dp.oldMag))

    # Constructor for the object
    # @args:
    #   1. params - dictionary with parameters
    #       a. 'threshold' - standard deviation threshold to call a peak a peak
    #   2. peakScores - input data queue containing the peak scores
    #   3. peakScoreData - list to put the peak score data
    #   4. peaks - output data queue containing identified peaks
    #   5. peakData - output data list to put identified peaks
    def __init__(self, params, peakScores, peakScoreData, peaks, peakData):

        super(PeakDetector, self).__init__()
        self.target = self.peakDetect

        # Internal data representations
        self.inputQueue = peakScores
        self.data = peakScoreData
        self.outputQueue = peaks
        self.dataout = peakData

        # Internal statistics
        self.n = 0
        self.mean = 0
        self.std = 0

        # Param unpacking
        self.threshold = params['threshold']











