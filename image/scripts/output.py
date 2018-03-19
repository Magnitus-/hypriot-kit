import os, sys

VERBOSITY_WEIGHT = {
    'quiet': 1,
    'info': 2,
    'debug': 3
}

def show(msg, level):
    verbosity = os.environ.get('VERBOSITY')
    if VERBOSITY_WEIGHT[level] <= VERBOSITY_WEIGHT[verbosity]:
        print msg
        sys.stdout.flush()
