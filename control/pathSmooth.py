# path : (real,real) array -> (real,real) array
# Takes a path of points on the grid and smooths it
# to be easier for the MOP to follow.

def pathSmooth(path):
    ### PARAMETERS ###

    # How much to smooth
    # (We'll average 2*smoothing+1 pts to get the smoothed ones)
    smoothing = 2

    ### CODE ###
    smoothPath = [None] * len(path)
    for i in range(len(path)):
        numPts = 0
        sumX = 0
        sumY = 0
        for ptIdx in range(i-smoothing,i+smoothing+1)
