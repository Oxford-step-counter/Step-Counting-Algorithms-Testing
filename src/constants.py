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

from src.infra.fancyPrinter import FancyPrinter

from src.windows.smoothing import CenterMovingAvg as Cma

from src.algorithms.peakDetection.peakFuncs import MaxDiff


# Class to contain constants
class Constants:

    THREAD_SLEEP_PERIOD = 0.01 # Note that this is in seconds. (10 ms)
    SAMPLE_PERIOD = 0.01 # Note this is in seconds. (10 ms)

    # Dictionary for types of smoothing windows
    SMOOTHING_WINDOWS = dict()
    SMOOTHING_WINDOWS['center_moving_avg'] = Cma

    # Dictionary for types of peakiness functions for windowed peak detection
    PEAKY_FUNCTIONS = dict()
    PEAKY_FUNCTIONS['max_diff'] = MaxDiff

    # Dictionary for graph iterables for UI
    UI_GRAPHS = dict()
    UI_GRAPHS['wpd'] = ['raw_data', 'smooth_data', 'peak_score_data', 'peak_data', 'confirmed_peak_data']

    # Dictionary for labels on axes.
    UI_GRAPHS_AXES = dict()

    UI_GRAPHS_AXES['wpd'] = dict()
    UI_GRAPHS_AXES['wpd']['raw_data'] = {'x' : 'time (ms)', 'y' : 'magnitude (m/s^2)'}
    UI_GRAPHS_AXES['wpd']['smooth_data'] = UI_GRAPHS_AXES['wpd']['raw_data']
    UI_GRAPHS_AXES['wpd']['peak_score_data'] = {'x' : 'time (ms)', 'y' : 'peak score'}
    UI_GRAPHS_AXES['wpd']['peak_data'] = UI_GRAPHS_AXES['wpd']['raw_data']
    UI_GRAPHS_AXES['wpd']['confirmed_peak_data'] = UI_GRAPHS_AXES['wpd']['raw_data']

    # Dictionary for type of lines on each plot.
    UI_GRAPHS_LINE = dict()

    UI_GRAPHS_LINE['wpd'] = dict()
    UI_GRAPHS_LINE['wpd'] = dict()
    UI_GRAPHS_LINE['wpd']['raw_data'] = {'marker': None, 'line': '-'}
    UI_GRAPHS_LINE['wpd']['smooth_data'] = UI_GRAPHS_LINE['wpd']['raw_data']
    UI_GRAPHS_LINE['wpd']['peak_score_data'] = UI_GRAPHS_LINE['wpd']['raw_data']
    UI_GRAPHS_LINE['wpd']['peak_data'] = {'marker': 'x', 'line': None}
    UI_GRAPHS_LINE['wpd']['confirmed_peak_data'] = UI_GRAPHS_LINE['wpd']['peak_data']

    # Dictionary for data about lines on each plot.
    UI_GRAPHS_POS = dict()

    UI_GRAPHS_POS['wpd'] = dict()
    UI_GRAPHS_POS['wpd']['raw_data'] = [231]
    UI_GRAPHS_POS['wpd']['smooth_data'] = [232, 234, 235]
    UI_GRAPHS_POS['wpd']['peak_score_data'] = [233]
    UI_GRAPHS_POS['wpd']['peak_data'] = [234]
    UI_GRAPHS_POS['wpd']['confirmed_peak_data'] = [235]

    THREAD_LOG = 'thread_log.txt'
    ERROR_LOG = 'error_log.txt'

    fp = FancyPrinter()
