# path : ((real,real), (real,real) array) -> real
# Returns the shortest distance from pos to path

def distance(pos, path):
    ### PARAMETERS ###

    # Number of points we want to consider
    # (we don't want to accidentally jump to another part of the path)
    numPts = 10

    ### CODE ###

    cutPath = path[:numPts] if numPts < len(path) else path
