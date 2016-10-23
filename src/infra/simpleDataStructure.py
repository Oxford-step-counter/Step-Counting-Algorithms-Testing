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

class Sds :

    #Constructor
    # @args:
    #   1. time - timestamp
    #   2. mag - magnitude of the signal
    def __init__(self, time, mag) :

        self.time = time
        self.mag = mag

    def getTime(self) :
        return self.time

    def getMag(self) :
        return self.mag

    def setTime(self, time) :
        self.time = time

    def setMag(self, mag) :
        self.mag = mag
