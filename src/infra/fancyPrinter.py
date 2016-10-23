class FancyPrinter :

    def __init__(self) :
        self.prev_len = 0

    def fprint(self, obj) :

        print(' ' * self.prev_len, end = '\r')
        print(str(obj), end = '\r')
        self.prev_len = len(str(obj))
