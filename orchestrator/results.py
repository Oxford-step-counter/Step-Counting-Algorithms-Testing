from logger import log
# Class to contain the results of each permutation of parameters.
# Will store the top 5 results.
class Results:

    def __init__(self, size):
        self.content = []
        self.errors = []
        self.maximum = []
        self.min_max = 0
        self.size = size

    def reset(self):
        self.content = []
        self.errors = []
        self.maximum = []
        self.min_max = 0

    def parse(self,content):
        if 'error' in content:
            self.errors.append(content)
            log(2, 'Results', 'Received score with error.')
        else:
            self.content.append(content)
            log(1, 'Results', 'New score received: ' + str(content['stats']['score']))
            # Determine if we are in the top 5.
            if len(self.maximum) < 5:
                self.maximum.append(content)
                if self.min_max > content['stats']['score']:
                    self.min_max = content['stats']['score']
            else:
                if content['stats']['score'] > self.min_max:
                    self.insertNewMax(content)

            if len(self.content) + len(self.errors) == self.size:
                # We have received all data points. Dump to file.
                with open('results.json', 'w') as outfile:
                    json.dump(self.maximum, outfile)

    def show(self):
        return self.maximum

    def get(self):
        return self.content

    def insertNewMax(self, content):

        log(1, 'Results', 'New maximum found!')

        # Find minimum in max.
        _min = 1000000000
        n = 0
        for i, maxValue in enumerate(self.maximum):
            if maxValue['stats']['score'] < _min:
                _min = maxValue['stats']['score']
                n = i

        # Remove minimum and insert new value
        del self.maximum[n]
        self.maximum.append(content)

        #Find minimum again
        _min = 1000000000
        n = 0
        for i, maxValue in enumerate(self.maximum):
            if maxValue['stats']['score'] < _min:
                _min = maxValue['stats']['score']
                n = i

        self.min_max = self.maximum[n]['stats']['score']
