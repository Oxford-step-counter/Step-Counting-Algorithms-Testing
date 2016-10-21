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
from infra.dataStructure import DataStructure

#Function to load in the accelerometer data from the CSV file.
def loadCSV(filepath) :

    data = []
    with open(filepath, 'r') as f :
        for line in f :
            s_line = line.split(',')
            ds = DataStructure(int(s_line[0]), float(s_line[2]), float(s_line[3]), float(s_line[4]))
            data.add(ds)

    return data
