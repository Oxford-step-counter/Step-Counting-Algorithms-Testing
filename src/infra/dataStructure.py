#========================================================================#
#
#       dataStructure.py
#       Jamieson Brynes
#       10/21/2016
#
#       This class contains the data structure format for a data point.
#
#=========================================================================#
import math

#Data structure for accelerometer data point.
class DataStructure :

    #Constructor
    # @args:
    #   1. time - timestamp
    #   2. x - x-coordinate of acceleration
    #   3. y - y-coordinate of acceleration
    #   4. z - z-coordinate of acceleration
    def __init__(self, time, x, y, z) :

        self.time = time
        self.x = x
        self.y = y
        self.z = z
        self.magnitude = None
        #Boolean for tracking if this data point was smoothed
        self.modified = False


    #Function to scale and shift time axis.
    # @args:
    #   1. startTime - time that the data trace started (time = 0 point)
    #   2. factor - the scaling factor for converting units. i.e. --> to go from ns to ms this should be 10^6
    def scaleTime(self, startTime, factor) :
        self.time = (self.time - startTime) / factor


    #Function to compute magnitude
    def computeMagnitude(self) :
        self.magnitude = math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2) + math.pow(self.z, 2))

    #Function to dump this data to a csv line entry
    def toCsv(self) :
        return str(self.time) + ',' + str(self.x) + ',' + str(self.y) + ',' + str(self.z) + '\n'


    #Getters and setters
    def setX(self, x) :
        self.x = x

    def setY(self, y) :
        self.y = y

    def setZ(self, z) :
        self.z = z

    def setTime(self, time) :
        self.time = time

    def setMagnitude(self, mag) :
        self.magnitude = mag

    def getX(self) :
        return self.x

    def getY(self) :
        return self.y

    def getZ(self) :
        return self.z

    def getTime(self) :
        return self.time

    def getMagnitude(self) :
        return self.magnitude
