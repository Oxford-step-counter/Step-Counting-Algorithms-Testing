
from threading import Thread

class MaxDiff:

    def __init__(self, params, smoothData, smoothDataList, peakScores):

        self.thread = None
        self.active = False
        self.completed = False

        self.inputQueue = smoothData
        self.data = smoothDataList

    def start(self):
        self.active = True
        self.thread = Thread(target=self.maxDiff, args=())
        self.thread.daemon = True
        self.thread.start()


    def stop(self):
        self.active = False

    def isRunning(self):
        return self.active and (True if (self.thread is not None and self.thread.isAlive) else False)

    def isDone(self):
        return self.completed

    def maxDiff(self):
        while self.active:
            if not self.inputQueue.isEmpty():

                ds = self.inputQueue.dequeue()

                if ds == 'end':
                    self.completed = True
                    self.active = False
                    return

                self.data.append(ds)
