import numpy as np

# pathSmooth : (real,real) array -> (real,real) array
# Takes a path of points on the grid and smooths it
# to be easier for the MOP to follow.

def pathSmooth(path):
    ### PARAMETERS ###

    # How much to smooth
    # (We'll average 2*smoothing+1 pts to get the smoothed ones)
    smoothing = 2

    ### CODE ###
    numPts = smoothing*2 + 1
    smoothPath = [None] * len(path)

    for i in range(len(path)):
        # Don't change first or last point
        if i == 0 or i == len(path) - 1:
            smoothPath[i] = path[i]
            continue

        # accumulators
        sumX = 0
        sumY = 0

        for ptIdx in range(i-smoothing,i+smoothing+1):
            # Get the pt, bounded so it's in the list
            pt = path[np.clip(ptIdx,0,len(path)-1)]

            sumX += pt[0]
            sumY += pt[1]

        smoothPath[i] = (sumX/numPts, sumY/numPts)

    return smoothPath
