#========================================================================#
#
#       plottableList.py
#       Jamieson Brynes
#       10/24/2016
#
#       This class contains the data structure format for a plottable list.
#       it resemble the subscriber/publisher design pattern for updates to
#       the graph. When a point is appended, we publish the update.
#
#=========================================================================#


class PlottableList:

    # Constructor for the object
    def __init__(self):

        # Interal lists for data and subscribers
        self._list = []
        self._subs = []

    # Method to subscribe to this list. Must provide a callback function and a identifier
    def subscribe(self, callback, name):

        self._subs.append([callback, name])

    # Method to add a datapoint
    def append(self, datapoint):

        self._list.append(datapoint)
        # Tell each subscriber that there is an update
        for sub in self._subs:
            sub[0](sub[1], self._list)

    # Implementations of list properties
    def __len__(self) :
        return len(self._list)

    def __getitem__(self, i):
        return self._list[i]
