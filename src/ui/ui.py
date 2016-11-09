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

import matplotlib.pyplot as plt


class UI:

    def __init__(self, algo):

        self.fig = plt.figure()
        self.subplots = {}
        name = algo.getName()
        lists = algo.getData()
        steps = algo.steps
        i = 0

        for l in lists:
            x = []
            y = []
            for dp in l:
                x.append(dp.time)
                y.append(dp.mag)

            l_name = Constants.UI_GRAPHS[name][i]
            axesData = Constants.UI_GRAPHS_AXES[name][l_name]
            positions = Constants.UI_GRAPHS_POS[name][l_name]
            lineData = Constants.UI_GRAPHS_LINE[name][l_name]
            for position in positions:

                if position not in self.subplots:
                    self.subplots[position] = self.fig.add_subplot(position)

                self.subplots[position].set_title(l_name)
                self.subplots[position].set_xlabel(axesData['x'])
                self.subplots[position].set_ylabel(axesData['y'])
                self.subplots[position].plot(x, y, marker=lineData['marker'], linestyle=lineData['line'])

            i += 1

        position = Constants.UI_GRAPHS_POS[name]['steps'][0]
        i = 0
        for step in steps:
            self.subplots[position].axvline(x=step, ymin=0, ymax=1)
            if i > 9:
                break
            i += 1
        plt.show()
