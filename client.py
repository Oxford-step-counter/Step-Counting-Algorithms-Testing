import sys
import json
import os
import time
from optparse import OptionParser

sys.dont_write_bytecode = True

from src.algorithms.peakDetection.windowedPeakDetection import Wpd


def main():


    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-i", "--input", dest="input", help="input CSV file")

    (options, args) = parser.parse_args(sys.argv)


    # Unpack params
    pre = {'inter_ts': 10, 'ts_factor': 1000000}
    filter = {'window_size':13, 'std':0.35, 'type':'gaussian'} #config['algorithm']['params']['filter']
    scoring = 	{'window_size':27, 'type':'mean_diff'} #config['algorithm']['params']['scoring']
    detection = {'threshold':1.2} #config['algorithm']['params']['detection']
    post = {'time_threshold':200} #config['algorithm']['params']['post']

    config = {}

    # Initialize results dictionary
    config['results'] = dict()

    # Initialize stats dictionary
    stats = dict()
    stats['steps'] = 0
    stats['ground_truth'] = 0
    config['stats'] = stats

    if options.input:
        algo = Wpd(options.input, pre, filter, scoring, detection, post)
        getAlgoResults(algo, config)

        print(config['stats']['steps'])

    else :
        print ("No input file provided")


def getAlgoResults(algorithm, config):

    algorithm.start()
    while algorithm.isRunning():
        time.sleep(1)

    # Algorithm is finished. Run comparison
    result = algorithm.compare()
    # Update stats
    config['stats']['steps'] += result[0]
    config['stats']['ground_truth'] += result[1]


if __name__ == "__main__":
    main()
