#========================================================================#
#
#       queue.py
#       Jamieson Brynes
#       10/21/2016
#
#       This class is designed to be a simple implementation of a queue
#       in Python.
#
#=========================================================================#

from collections import deque


# Basic implementation of queue wrapping around the deque class.
class Queue:

    def __init__(self):
        self.queue = deque()

    def isEmpty(self):
        return len(self.queue) == 0
    
    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        return self.queue.popleft()

    def size(self):
        return len(self.queue)

    def __getitem__(self, i):
        return self.queue[i]

    def __len__(self):
        return len(self.queue)
