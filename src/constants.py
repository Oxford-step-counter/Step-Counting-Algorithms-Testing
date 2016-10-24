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

    THREAD_SLEEP_PERIOD = 0.01 # Note that this is in seconds. (30 ms)
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
    UI_GRAPHS_AXES['raw_data'] = {'x' : 'time (ms)', 'y' : 'magnitude (m/s^2)'}
    UI_GRAPHS_AXES['smooth_data'] = UI_GRAPHS_AXES['raw_data']
    UI_GRAPHS_AXES['peak_score_data'] = {'x' : 'time (ms)', 'y' : 'peak score'}
    UI_GRAPHS_AXES['peak_data'] = UI_GRAPHS_AXES['raw_data']
    UI_GRAPHS_AXES['confirmed_peak_data'] = UI_GRAPHS_AXES['raw_data']

    # Dictionary for data about lines on each plot.
    UI_GRAPH_DATA = dict()
    UI_GRAPH_DATA['raw_data'] = [['raw_data', 'line']]
    UI_GRAPH_DATA['smooth_data'] = [['smooth_data', 'line']]
    UI_GRAPH_DATA['peak_score_data'] = [['peak_score_data', 'line']]
    UI_GRAPH_DATA['peak_data'] = [['smooth_data', 'line'], ['peak_data', 'point']]
    UI_GRAPH_DATA['confirmed_peak_data'] = [['smooth_data', 'line'], ['confirmed_peak_data', 'point']]

    THREAD_LOG = 'thread_log.txt'
    ERROR_LOG = 'error_log.txt'

    fp = FancyPrinter()
