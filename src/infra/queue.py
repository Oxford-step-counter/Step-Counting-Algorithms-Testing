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


#Basic implementation of queue 
class Queue :

    def __init__(self) :
        self.items = []

    def isEmpty(self) :
        return self.items == []

    def enqueue(self, item) :
        return self.items.insert(0,item)

    def dequeue(self) :
        return self.items.pop()

    def size(self) :
        return len(self.items)
