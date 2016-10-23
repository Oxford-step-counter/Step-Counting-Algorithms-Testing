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

    def __init__(self, time, x, y, z) :

        self.time = time
        self.x = x
        self.y = y
        self.z = z
        self.magnitude = None
        #Boolean for tracking if this data point was smoothed
        self.modified = False

    #Function to scale and shift time axis.
    def scaleTime(self, startTime, factor) :

        self.time = (self.time - startTime) / factor

    #Function to compute magnitude
    def computeMagnitude(self) :
        self.magnitude = math.pow(self.x, 2) + math.pow(self.y, 2) + math.pow(self.z, 2)

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
