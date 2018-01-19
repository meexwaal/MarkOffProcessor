import cv2
import numpy as np
#from calibrate import *
from path_planning import *

masking = False
maskcount = 61
maskframes = 60
mask = None
blurSize = 5

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
      count = 0
      for k in range(i, min(i + blocksize,len(arr))):
        for l in range(j, min(j + blocksize,len(arr[0]))):
          if arr[k][l] == 0:
            count = count + 1
      if count >= 16:
        ink = 0
      grid[i // blocksize][j // blocksize] = ink
  return grid

def processImage(frame):
    global blurSize,maskcount,mask
    # convert to gray
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # apply median filter
    img = cv2.medianBlur(img,blurSize)
    # apply adaptive gaussian thresholding
    img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,11,2)
    # apply median filter
    img = cv2.medianBlur(img,blurSize)
    # handle masking
    if masking:
      if maskcount < maskframes:
        maskcount = maskcount + 1
        mask = cv2.bitwise_and(img,mask)
      if maskcount == maskframes:
        mask = cv2.erode(mask,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)))
        maskcount = maskcount + 1
        blurSize = 3
      img = cv2.bitwise_or(img,cv2.bitwise_not(mask))
      cv2.imshow('Mask',mask)

    return img

def toggleMask(img):
  global masking, blurKernel, maskcount, mask
  if masking:
    masking = False
    blurKernel = 5
  else:
    masking = True
    maskcount = 0
    mask = img

def doneBuilding():
  return maskcount > maskframes

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

def coordChange(p,blocksize):
  (x,y) = p
  return (y*blocksize+blocksize//2,x*blocksize+blocksize//2)

def findPath(img,start):
    #TODO
    blocksize = 8
    mat = ImageBlocky(img,blocksize)
    goodMoves = ImageToBlackList(mat)
    mask = cv2.circle(mask,start,48,1,-1)
    badMoves = ImageToBlackList(ImageBlocky(mask,blocksize))
    img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    for g in goodMoves:
        p = coordChange(g,blocksize)
        cv2.line(img,p,p,(0,255,0))
    for b in badMoves:
        p = coordChange(b,blocksize)
        cv2.line(img,p,p,(0,0,255))
    (x,y) = start
    path = planPath((x//blocksize,y//blocksize),goodMoves,badMoves,len(mat),len(mat[0]))
    last = None
    for i in range(len(path)):
        p = coordChange(path[i],blocksize)
        path[i] = p
        if last is not None:
            cv2.line(img,last,p,(0,255,0)if i==1 else(255,0,0))
        last = p
    cv2.line(img,start,start,(255,0,0), 3)
    cv2.imshow('path', img)
    cv2.waitKey(0)
    return path
          
