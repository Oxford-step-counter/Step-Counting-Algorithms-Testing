#========================================================================#
#
#       utils.py
#       Jamieson Brynes
#       10/21/2016
#
#       This class contains various utility functions that do not belong
#       in a class anywhere.
#
#=========================================================================#
from src.infra.dataStructure import DataStructure
from src.infra.simpleDataStructure import Sds


# Function to load in the accelerometer data from the CSV file.
# @args:
#   1. filepath - path to the .csv file location
# TODO : Add exception handling
def loadCsv(filepath):

    data = []
    with open(filepath, 'r') as f :
        for line in f :
            s_line = line.split(',')
            ds = DataStructure(int(s_line[0]), float(s_line[2]), float(s_line[3]), float(s_line[4]))
            data.append(ds)

    return data


# Function to create empty files as clean logs on each run.
def initLogs():

    # Create clean files
    with open('threadlog.txt', 'w') as f:
        pass
    with open('errorlog.txt', 'w') as f:
        pass


# Function for logging events with respect to thread.
# @args:
#   1. s - string to write to log.
def threadLog(s):
    with open('threadlog.txt', 'a') as f:
        f.write(s)
        f.write('\r\n')


# Function for logging errors
# @args :
#   1. s - string to write to log
def errorLog(s):
    with open('errorlog.txt', 'a') as f :
        f.write(s)
        f.write('\r\n')


# Linear interpolation function. Simple implementation.
# @args:
#   1. dp1 - datapoint one, assume dataStructure type
#   2. dp2 - datapoint two, assume dataStructure type
#   3. time - interpolation time
def linearInterp(dp1, dp2, time):

    time1 = dp1.getTime()
    time2 = dp2.getTime()
    dt = time2 - time1

    value1 = dp1.getMagnitude()
    value2 = dp2.getMagnitude()
    dv = value2 - value1

    slope = dv / dt

    new_mag = slope * (time - time1) + value1

    return Sds(time, new_mag)


# Function to print a queue of data to a .csv file
# @args:
#   1. queue - Queue or list object to iterate over.
#   2. filename - name of the csv file to be created.
def printToCsv(queue, filename):

    with open(filename, 'w') as f:

        for i in range(0,len(queue)):
            f.write(queue[i].toCsv())
