

def formatResults(results):

    # Take in the list of tuples and return the accuracies.
    
    ret = ""
    
    for res in results:

        (rid, pid, acc) = res
        ret += "<p>" + str(acc) + "</p>"

    return ret
