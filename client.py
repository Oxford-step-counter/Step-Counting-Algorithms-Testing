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
        stats['detected'] = 0
        stats['missed'] = 0
        stats['extra'] = 0
        config['stats'] = stats

        # Start new batch sim
        for data in databank:
            fp = data + '/'
            algo = Wpd(fp, pre, filter, scoring, detection, post)
            getAlgoResults(algo, config)

        # Return data
        # Calculate final statistics
        config['stats']['accuracy'] = config['stats']['confirmed'] / config['stats']['steps']
        config['stats']['false_positive_rate'] = config['stats']['extra'] / config['stats']['confirmed']
        config['stats']['false_negative_rate'] = config['stats']['missed'] / config['stats']['steps']

        #Calculate algorithm score
        score = 0
        n = 0
        for key in list(config['results'].keys()):
            score += config['results'][key]['score']
            n += 1
        config['stats']['score'] = score / n

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
    config['stats']['confirmed'] += result[1]
    config['stats']['extra'] += result[2]
    config['stats']['missed'] += result[3]

    # Add entry to results.
    config['results'][algorithm.filelocation] = dict()
    # Accuracy
    config['results'][algorithm.filelocation]['accuracy'] = result[1] / result[0]
    # False Positive Rate = extra / detected
    config['results'][algorithm.filelocation]['false_positive'] = result[2] / result[1]
    # False Negative Rate = missed / num_steps
    config['results'][algorithm.filelocation]['false_negative'] = result[3] / result[0]

    # Calculate rating.
    config['results'][algorithm.filelocation]['score'] = 2 - ((abs(result[1] - result[0])) / result[0]) - (config['results'][algorithm.filelocation]['false_positive'] + config['results'][algorithm.filelocation]['false_negative'])

if __name__ == "__main__":
    main()
