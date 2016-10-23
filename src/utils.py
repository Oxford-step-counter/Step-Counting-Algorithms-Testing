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
from src.constants import Constants

#Function to load in the accelerometer data from the CSV file.
def loadCSV(filepath) :

    data = []
    with open(filepath, 'r') as f :
        for line in f :
            s_line = line.split(',')
            ds = DataStructure(int(s_line[0]), float(s_line[2]), float(s_line[3]), float(s_line[4]))
            data.append(ds)

    return data


#Function for logging events with respect to thread.
def threadLog(s) :
    with open(Constants.threadlog) as f :
        f.write(s)
        f.write('\r\n')


def linearInterp(dp1, dp2, time) :

    time1 = dp1.getTime()
    time2 = dp2.getTime()
    dt = time2 - time1

    value1 = dp1.getMagnitude()
    value2 = dp2.getMagnitude()
    dv = value2 - value1

    slope = dv / dt

    new_mag = slope * (time - time1)

    return Sds(time, new_mag)
