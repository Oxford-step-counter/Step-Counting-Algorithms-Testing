# ======================================================================== #
#
#       comparator.py
#       Jamieson Brynes
#       10/27/2016
#
#       This file contains the comparison logic for comparing the step's
#       counted vs. the steps recorded.
#
# ========================================================================= #

from src import utils


# Function to compare, it will return a tuple of values
# @args:
#   1. filepath - file location of the step counter truth data.
#   2. confirmedPeaks - list of data structures with confirmed times.
#   3. timeData - dictionary of time related values
#       a. 'threshold' - maximum difference between a peak to call it acceptable
#       b. 'offset' - time offset
#       c. 'scale' - time scaling factor
# @return: (accuracy, falsePositiveRate, falseNegativeRate)
#   1. accuracy - float containing the percentage of accuracy.
#   2. falsePositiveRate - number of steps that were incorrectly identified
#   3. falseNegativeRate - number of steps that were not picked up.
def compare(stepsMaster, confirmedPeaks, threshold):

    # Make a copy of the confirmed peaks and steps
    peaks = []
    for peak in confirmedPeaks:
        peaks.append(peak)

    steps = []
    for step in stepsMaster:
        steps.append(step)

    confirmedSteps = 0
    falsePositives = 0
    num_steps = len(steps)
    num_peaks = len(confirmedPeaks)

    while peaks:
        time = peaks.pop(0).time
        for step in steps:
            if step >= time and abs(time - step) < threshold:
                confirmedSteps += 1
                steps.remove(step)
                break
        else:
            falsePositives += 1

    accuracy = confirmedSteps / num_steps
    falsePositiveRate = falsePositives / num_peaks
    falseNegativeRate = (num_steps - confirmedSteps) / num_steps

    message = "Overall accuracy: " \
              + str(accuracy) \
              + "\nFalse Positive Rate: " \
              + str(falsePositiveRate) \
              + "\nFalse Negative Rate" \
              + str(falseNegativeRate)

    return [num_steps, num_peaks, falsePositives, num_steps - confirmedSteps]
