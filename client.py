import sys
import requests
import json
import os
import time
sys.dont_write_bytecode = True

from src.algorithms.peakDetection.windowedPeakDetection import Wpd


def main():

    # Set up stuff
    get_url = 'http://api.jamiebrynes.com/get_next'
    return_url = 'http://api.jamiebrynes.com/return'
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    databank = getDataBank('./data/')
    # Check server for new value
    response = requests.get(get_url)
    config = response.json()
    while 'status' not in config:

        print(config)

        # Unpack params
        pre = config['algorithm']['params']['pre']
        filter = config['algorithm']['params']['filter']
        scoring = config['algorithm']['params']['scoring']
        detection = config['algorithm']['params']['detection']
        post = config['algorithm']['params']['post']

        # Initialize results dictionary
        config['results'] = dict()

        # Initialize stats dictionary
        stats = dict()
        stats['steps'] = 0
        stats['ground_truth'] = 0
        config['stats'] = stats

        # Start new batch sim
        for data in databank:
            fp = data + '/'
            algo = Wpd(fp, pre, filter, scoring, detection, post)
            getAlgoResults(algo, config)

        # Calculate algorithm accuracy
        score = 0
        n = 0
        for key in list(config['results'].keys()):
            score += config['results'][key]['accuracy']
            n += 1
        config['stats']['accuracy'] = score / n

        res = requests.post(return_url, headers=headers, data=json.dumps(config))

        response = requests.get(get_url)
        config = response.json()


def getDataBank(data_path):

    # Find all subdirectories in the data path
    dirs = [os.path.join(data_path, d) for d in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, d))]
    return dirs


def getAlgoResults(algorithm, config):

    print('Starting new algorithm')
    algorithm.start()
    while algorithm.isRunning():
        time.sleep(1)

    # Algorithm is finished. Run comparison
    result = algorithm.compare()
    # Update stats
    config['stats']['steps'] += result[0]
    config['stats']['ground_truth'] += result[1]

    # Add entry to results.
    config['results'][algorithm.filelocation] = dict()
    # Accuracy
    config['results'][algorithm.filelocation]['accuracy'] = 1 - abs(result[0] - result[1]) / result[1]

if __name__ == "__main__":
    main()
