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
from src.constants import Constants
import src.utils as utils

class InputPipe :

    def __init__(self, filepath) :
        self.filepath = filepath

    def attachQueue(self, queue) :

        self.queue = queue

    def start(self) :

        if hasattr(self, 'queue') :
            try :
                self.thread = Thread(target = self.pipeInput, args = ())
                self.thread.daemon = True
                self.thread.start()
            except :
                print('Error: Cannot start piping thread')
        else :

            print('No queue attached')

    def isRunning(self) :

        if hasattr(self, 'thread') :
            return self.thread.isAlive()
        else :
            return False

    def stop(self) :

        if self.thread :
            self.thread.stop()

    def pipeInput(self) :

        data = utils.loadCSV(self.filepath)

        for datapoint in data :
            self.queue.enqueue(datapoint)
            time.sleep(Constants.samplePeriod)
