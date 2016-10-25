#========================================================================#
#
#       simpleDataStructure.py
#       Jamieson Brynes
#       10/21/2016
#
#       This class contains the data structure format for a data point
#       after preprocessing.
#
#=========================================================================#


class Sds:

    # Constructor
    # @args:
    #   1. time - timestamp
    #   2. mag - magnitude of the signal
    #   3. old_mag (optional) - old magnitude, for when we edit magnitude (peak scores)
    def __init__(self, time, mag, old_mag=None):

        self.time = time
        self.mag = mag
        self.oldMag = old_mag

    # Output CSV line
    def toCsv(self):
        return str(self.time) + ',' + str(self.mag) + '\n'

    # Getters and setters
    def getTime(self):
        return self.time

    def getMagnitude(self):
        return self.mag

    def getOldMagnitude(self):
        return self.oldMag

    def setTime(self, time):
        self.time = time

    def setMagnitude(self, mag):
        self.mag = mag

    def setOldMagnitude(self, old_mag):
        self.oldMag = old_mag
