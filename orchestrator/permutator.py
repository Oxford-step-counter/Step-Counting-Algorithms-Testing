import json
import time
from logger import log

class Permutator():

    def __init__(self, db):
        self.count = 0
        self.permutations = []
        self.permutation_details = Permutator.loadJson("permutation_details.json", self.permutations, db)
        self.start_time = None
        log(1, 'Permutator', 'Permutator initialized')

    def getNext(self):
        if self.start_time == None:
            self.start_time = time.time()
        if self.count < len(self.permutations):
            data = self.permutations[self.count]
        else:
            data = {'status': 'end'}
        self.count += 1
        log(1, 'Permutator', 'Sending next permutation. ' + str(self.count) + '/' + str(len(self.permutations)))
        log(1, 'Permutator', 'Time elapsed: ' + Permutator.timeConvert(time.time() - self.start_time))
        log(1, 'Permutator', 'Estimated Time Left: ' + Permutator.estimateTimeLeft(self.count, len(self.permutations), time.time() - self.start_time))
        return data

    def reset(self):
        self.count = 0
        self.start_time = None
        log(1, 'Permutator', 'Permutator reset.')
        return True

    @staticmethod
    def timeConvert(seconds):

        minutes = int(seconds) / 60
        _seconds = int(seconds) % 60
        _minutes = int(minutes % 60)
        _hours = int(minutes / 60)

        return str(_hours) + ":" + str(_minutes) + ":" + str(_seconds)

    @staticmethod
    def estimateTimeLeft(current, total, elapsed):

        estimated_left = (elapsed * total / current) - elapsed
        r = Permutator.timeConvert(estimated_left)
        return r

    @staticmethod
    def loadJson(filepath, permutations, db):
    
        permutation_data = json.load(open(filepath, 'r'))

        permutations_temp = []
        permutations_temp2 = []

        # Permute over each type and merge
        filter_data = permutation_data['filter']
        Permutator.permuteSection(permutations_temp, filter_data, 'filter')
        scoring_data = permutation_data['scoring']
        Permutator.permuteSection(permutations_temp2, scoring_data, 'scoring')
        Permutator.mergePermutations(permutations_temp, permutations_temp2)
        detection_data = permutation_data['detection']
        Permutator.permuteSection(permutations_temp2, detection_data, 'detection')
        Permutator.mergePermutations(permutations_temp, permutations_temp2)
        post_data = permutation_data['post']
        Permutator.permuteSection(permutations_temp2, post_data, 'post')
        Permutator.mergePermutations(permutations_temp, permutations_temp2)

        # Add the standard prefix onto the beginning.
        for perm in permutations_temp:

            key = db.addParameterSet(perm)

            d = dict()
            d['algorithm'] = dict()
            d['algorithm']['name'] = 'wpd'
            d['algorithm']['params'] = dict()
            d['algorithm']['params']['key'] = key
            d['algorithm']['params']['pre'] = {'inter_ts': 10, 'ts_factor': 1000000}
            for key in perm:
                d['algorithm']['params'][key] = perm[key]
            permutations.append(d)

    @staticmethod
    def mergePermutations(temp1, temp2):

        temp = temp1[:]
        temp1[:] = []
        for t in temp:
            for t2 in temp2:
                d = dict()
                for key in list(t.keys()):
                    d[key] = t[key]
                for key in list(t2.keys()):
                    d[key] = t2[key]
                temp1.append(d)

        temp2[:] = []


    @staticmethod
    def permuteSection(permutations_temp, data, key):

        # Unpack all params.
        for typ in data.keys():
            permutables = []
            statics = []
            type_data = data[typ]
            for param in type_data.keys():
                if type(type_data[param]) is int or type(type_data[param]) is float:
                    statics.append({param: type_data[param]})
                else:
                    permutables.append({param: type_data[param]})

            Permutator.recursiveConstruct(permutations_temp, key, typ, statics, permutables)



    @staticmethod
    def recursiveConstruct(permutations_temp, key, typ, statics, permutables):

        # Recursion base case. Build the dictionary
        if len(permutables) == 0:
            d = dict()
            d[key] = dict()
            p = d[key]
            if typ != 'solo':
                p['type'] = typ
            for static in statics:
                p[list(static.keys())[0]] = static[list(static.keys())[0]]
            permutations_temp.append(d)
            return

        p = permutables[:]
        s = statics[:]
        permutable = p.pop()
        key1 = list(permutable.keys())[0]
        data = permutable[key1].copy()
        while data['min'] <= data['max']:
            s.append({key1: data['min']})
            Permutator.recursiveConstruct(permutations_temp, key, typ, s, p)
            data['min'] += data['step']
            s = statics[:]
