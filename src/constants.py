#========================================================================#
#
#       constants.py
#       Jamieson Brynes
#       10/21/2016
#
#       This class contains all of the constants for the step counting
#       programs.
#
#========================================================================#

#from src.windows.smoothing import CenterMovingAvg as Cma
from src.infra.fancyPrinter import FancyPrinter

#Class to contain constants
class Constants :

    #Debug toggle
    DEBUG = True

    THREAD_SLEEP_PERIOD = 0.03 #Note that this is in seconds. (30 ms)
    SAMPLE_PERIOD = 0.01 #Note this is in seconds. (10 ms)

    #Dictionary for types of smoothing windows
    SMOOTHING_WINDOWS = {}
    #SMOOTHING_WINDOWS['center_moving_avg' : Cma]

    #Dictionary for types of peakiness functions for windowed peak detection
    PEAKY_FUNCTIONS = {}


    threadlog = 'thread_log.txt'

    fp = FancyPrinter()
