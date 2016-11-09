#========================================================================#
#
#       dataStructure.py
#       Jamieson Brynes
#       10/22/2016
#
#       This class contains a class for printing data in place in the
#       console. i.e. - if you wanted a updating ticker.
#
#=========================================================================#


class FancyPrinter :

    def __init__(self) :
        self.prev_len = 0

    # Print function. Takes any object that can be turned into a string.
    # Overwrites the previous message with spaces to erase it and then
    # returns to the start of the line.
    def fprint(self, obj):

        print(' ' * self.prev_len, end='\r')
        print(str(obj), end='\r')
        self.prev_len = len(str(obj))
