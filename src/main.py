import sys
import time
import json
sys.dont_write_bytecode = True

from src.algorithms.peakDetection.windowedPeakDetection import Wpd
#from src.ui.ui import UI


def main():

    # Load json configuration
    config = json.load(open("../config.json", 'r'))

    algo = None

    if config['algorithm']['name'] == 'wpd':
        fp = config['file_path']
        pre = config['algorithm']['params']['pre']
        filter = config['algorithm']['params']['filter']
        scoring = config['algorithm']['params']['scoring']
        detection = config['algorithm']['params']['detection']
        post = config['algorithm']['params']['post']

        algo = Wpd(fp, pre, filter, scoring, detection, post)

    else:
        print("Configuration file specifies an unknown algorithm: " + config['algorithm'['name']])
        return

    print("Starting algorithm")
    algo.start()

    while algo.isRunning():
        time.sleep(1)

    print("Algorithm complete. Running comparison.")
    #result = algo.compare()
    #print(result)
    #print(len(algo.confirmedPeaks))
    #print(len(algo.steps))
    #ui = UI(algo)


# Entry point
if __name__ == "__main__":
    main()