#========================================================================#
#
#       inputPipe.py
#       Jamieson Brynes
#       10/21/2016
#
#       This class is designed to simulate the real time collection of data
#       points. It will deposit the data into a queue at a fixed sampling
#       rate.
#
#=========================================================================#

from threading import Thread
import time
from constants import Constants
import utils

class InputPipe :

    def __init__(self, filepath) :
        self.filepath = filepath

    def attachQueue(self, queue) :

        self.queue = queue

    def start(self) :

        if self.queue :
            try :
                self.thread = Thread(target = self.pipeInput, args = ())
                self.thread.start()
            except :
                print 'Error: Cannot start piping thread'
        else :

            print 'No queue attached'


    def stop(self) :

        if self.thread :
            self.thread.stop()

    def pipeInput(self) :

        self.data = utils.loadCSV(self.filepath)

        for datapoint in self.data :
            self.queue.add(data)
            time.sleep(Constants.samplePeriod)
