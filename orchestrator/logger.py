from datetime import datetime

infoLevel = dict()
infoLevel[0] = "DEBUG"
infoLevel[1] = "INFO"
infoLevel[2] = "WARN"
infoLevel[3] = "ERROR"

def log(level,src,msg):
    """[This is the logging functionality for the backend api.]

    [It takes in three arguments, the info level, the source of the message, and the message itself to display. It then formats a date and outputs the message to the console.

    The info level is decoded by a helper function.]

    Arguments:
        level {int} -- [This describes the level of the message: DEBUG, INFO, WARN, ERR]
        src {string} -- [This describes the source of the message]
        msg {string} -- [This is the message content]
    """

    d = decodeTime()
    line = "[{0}] [{1}] [{2}] {3}".format(decodeLevel(level), d, src, msg)
    print(line)


def decodeTime():
    """[This function returns the formatted date string for the logging message]"""

    d = datetime.today()
    return "{0}-{1}-{2} {3}:{4}:{5}".format(str(d.year), str(d.month), str(d.day), str(d.hour), str(d.minute), str(d.second))

def decodeLevel(level):
    """[This function decodes the level of the message.]

    [We take in a level and decode it to the correct level with a simple mapping.
        0 - DEBUG
        1 - INFO
        2 - WARN
        3 - ERROR
        Other - UNKNOWN
    ]

    Arguments:
        level {[type]} -- [description]
    """

    if level in infoLevel:
        return infoLevel[level]
    return "UNKNOWN"
