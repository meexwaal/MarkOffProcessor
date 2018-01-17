import cv2
import numpy as np

def ImageToBlackList(mat):
  list = []
  for i in range(len(mat)):
    for j in range(len(mat[0])):
      if mat[i][j] == 0:
        list.append((i, j))
  return list

def ImageBlocky(arr, blocksize):
  grid = [[0 for i in range(len(arr[0]) // blocksize + 1)] for j in range(len(arr) // blocksize + 1)]
  for i in range(0, len(arr), blocksize):
    for j in range(0, len(arr[0]), blocksize):
      ink = 255
      for k in range(i, min(i + blocksize,len(arr))):
        for l in range(j, min(j + blocksize,len(arr))):
          if arr[k][l] == 0:
            ink = 0
      grid[i // blocksize][j // blocksize] = ink
  return grid

def processImage(frame):
    img = frame
    # get background
    fgbg.getBackgroundImage(img)
    # convert to gray
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # apply median filter
    img = cv2.medianBlur(img,5)
    # apply adaptive gaussian thresholding
    img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,11,2)
    # apply median filter
    img = cv2.medianBlur(img,5)

    return img

def findRobot(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of color in HSV
    # currently HOT PINK
    lower_color = np.array([150,50,50])
    upper_color = np.array([180,255,255])
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_color, upper_color)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    # If not enough color detected, don't draw centroid
    TRACKER_THRESHOLD = 500

    # Calculate centroid of mask
    M = cv2.moments(mask)
    if M["m00"]/255 >= TRACKER_THRESHOLD:
        cx = int(M["m10"]/M["m00"])
        cy = int(M["m01"]/M["m00"])
        return cx,cy
    else:
        return None

def findPath(img,start):
    #TODO
    blocksize = 11
    mat = ImageBlocky(img,blocksize)
    goodMoves = ImageToBlackList(mat)
    path = planPath(start,goodMoves,[],len(mat),len(mat[0]))
    return path
          
#jdef GridToImage(grid):
#  Mat m(len(grid[0]), len(grid), CV_32SC1, grid)
#  return m
