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
        self.magnitude = self._computeMagnitude()

    #Function to scale and shift time axis.
    def scaleTime(self, startTime, factor) :

        self.time = (self.time - startTime) / factor

    #Internal function to compute magnitude
    def _computeMagnitude(self) :
        return math.pow(self.x, 2) + math.pow(self.y, 2) + math.pow(self.z, 2)

    #Getters and setters
    def setX(self, x) :
        self.x = x

    def setY(self, y) :
        self.y = y

    def setZ(self, z) :
        self.z = z

    def setMagnitude(self, mag) :
        self.magnitude = mag

    def getX(self) :
        return self.x

    def getY(self) :
        return self.y

    def getZ(self) :
        return self.z
