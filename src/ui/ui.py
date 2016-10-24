#========================================================================#
#
#       ui.py
#       Jamieson Brynes
#       10/24/2016
#
#       This class contains the UI master object. This initializes the UI
#       and handles UI updates and passes to the correct object
#
#========================================================================#

from src.constants import Constants
from src.algorithms.peakDetection.windowedPeakDetection import Wpd

import matplotlib.pyplot as plt


class UI:

    def __init__(self, algo):

        self.fig = plt.figure()
        self.subplots = {}
        if isinstance(algo, Wpd):
            self.handle_wpd(algo)
        plt.show()

    def handle_wpd(self, wpd):

        lists = [wpd.data, wpd.preprocessData, wpd.smoothedData, wpd.peakScoreData, wpd.peakData, wpd.confirmedPeaks]
        i = 0
        for l in lists:
            x = []
            y = []
            for dp in l:
                x.append(dp.time)
                y.append(dp.mag)

            name = Constants.UI_GRAPHS['wpd'][i]
            axesData = Constants.UI_GRAPHS_AXES['wpd'][name]
            positions = Constants.UI_GRAPHS_POS['wpd'][name]
            lineData = Constants.UI_GRAPHS_LINE['wpd'][name]
            for position in positions:

                if position not in self.subplots:
                    self.subplots[position] = self.fig.add_subplot(position)

                self.subplots[position].set_title(name)
                self.subplots[position].set_xlabel(axesData['x'])
                self.subplots[position].set_ylabel(axesData['y'])
                self.subplots[position].plot(x,y,marker=lineData['marker'],linestyle=lineData['line'])

            i += 1
