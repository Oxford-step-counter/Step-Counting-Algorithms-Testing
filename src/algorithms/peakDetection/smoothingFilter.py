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
import math

from src.infra.workerThread import WorkerThread
from src.infra.queue import Queue
from src.infra.simpleDataStructure import Sds

from scipy import special


class SmoothingFilter(WorkerThread):

    def centeredMovingAvg(self):
        self.windowSize = self.params['window_size']
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
                    new_dp = Sds(self.window[int(self.windowSize / 2)].time, ssum / self.windowSize, self.window[int(self.windowSize / 2)].mag)
                    self.outputQueue.enqueue(new_dp)
                    self.window.dequeue()

    def hann(self):

        self.windowSize = self.params['window_size']
        self.hann_window = SmoothingFilter.hannCoeffs(self.windowSize)
        self.hann_sum = sum(self.hann_window)

        while self.active:
            if not self.inputQueue.isEmpty():

                # Get next dp
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
                        ssum += self.window[i].mag * self.hann_window[i]
                    # Average of all points in the window
                    new_dp = Sds(self.window[int(self.windowSize / 2)].time, ssum / self.hann_sum, self.window[int(self.windowSize / 2)].mag)
                    self.outputQueue.enqueue(new_dp)
                    self.window.dequeue()

    def gaussian(self):

        self.windowSize = self.params['window_size']
        self.std = self.params['std']
        self.gauss_window = SmoothingFilter.gaussianCoeffs(self.windowSize, self.std)
        self.gauss_sum = sum(self.gauss_window)

        while self.active:
            if not self.inputQueue.isEmpty():

                # Get next dp
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
                        ssum += self.window[i].mag * self.gauss_window[i]
                    # Average of all points in the window
                    new_dp = Sds(self.window[int(self.windowSize / 2)].time, ssum / self.gauss_sum, self.window[int(self.windowSize / 2)].mag)
                    self.outputQueue.enqueue(new_dp)
                    self.window.dequeue()

    def kaiserBessel(self):
        self.windowSize = self.params['window_size']
        self.cutoff_freq = self.params['cutoff_freq']
        self.sample_freq = self.params['sample_freq']
        self.filter_coeff = SmoothingFilter.kaiserBesselCoeffs(self.windowSize, self.cutoff_freq, self.sample_freq)
        self.filter_sum = sum(self.filter_coeff)

        while self.active:
            if not self.inputQueue.isEmpty():

                # Get next dp
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
                        ssum += self.window[i].mag * self.filter_coeff[i]
                    # Average of all points in the window
                    new_dp = Sds(self.window[int(self.windowSize / 2)].time, ssum / self.filter_sum, self.window[int(self.windowSize / 2)].mag)
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
        self.params = params
        self.typ = params['type']

        # Internal buffer
        self.window = Queue()

        # Set correct target
        if self.typ == 'hann':
            self.target = self.hann
        elif self.typ == 'gaussian':
            self.target = self.gaussian
        elif self.typ == 'kaiser_bessel':
            self.target = self.kaiserBessel
        else:
            self.target = self.centeredMovingAvg

    @staticmethod
    def hannCoeffs(windowSize):

        window = []
        for n in range(windowSize):
            value = 0.5 * (1 - math.cos(2*math.pi * n / (windowSize - 1)))
            window.append(value)
        return window

    @staticmethod
    def gaussianCoeffs(windowSize, std):
        window = []

        for n in range(windowSize):
            value = math.exp(-0.5 * math.pow((n - (windowSize - 1) / 2) / (std * (windowSize - 1) / 2), 2))
            window.append(value)

        return window

    @staticmethod
    def kaiserBesselCoeffs(windowSize, cutoff_f, sampling_f):
        coeffs = []
        Np = (windowSize - 1) / 2

        # Assume we always want a attenuation of 60dB at cutoff frequency
        alpha = 5.65326
        Io_alpha = special.iv(0, alpha)

        # Calculate Kaiser-Bessel window coefficients
        window = []
        for i in range(0, windowSize):
            val = alpha * math.sqrt(1 - math.pow((i - Np) / Np, 2))
            window.append(special.iv(0, val) / Io_alpha)

        # Sinc function coefficients
        sinc = []
        for i in range(0, windowSize):
            val = 2 * (i - Np) * cutoff_f / sampling_f
            sinc.append(SmoothingFilter.sinc(val))

        # Multiple the coeffs together
        for i in range(0, windowSize):
            coeffs.append(window[i] * sinc[i])

        return coeffs

    @staticmethod
    def sinc(x):
        if x == 0:
            return 1
        else:
            return math.sin(math.pi * x) / (math.pi * x)

