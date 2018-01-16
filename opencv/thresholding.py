import cv2
import numpy as np
from matplotlib import pyplot as plt
from image_processing import *
from path_planning import *

cap = cv2.VideoCapture(1)

feed = 0
blockSize = 11
C = 2
kern = 5

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);

    img = gray
    img = cv2.medianBlur(img,5)

    if feed == 1:
        ret,img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    elif feed == 2:
        img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,blockSize,C)
    elif feed >= 3:
        img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,blockSize,C)

    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(kern,kern))
    if feed == 4:
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    elif feed == 5:
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    titles = ['Original Image', 'Global Thresholding (v = 127)',
            'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']

    cv2.imshow('frame',img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('1'):
        feed = 0
    elif key == ord('2'):
        feed = 1
    elif key == ord('3'):
        feed = 2
    elif key == ord('4'):
        feed = 3
    elif key == ord('5'):
        feed = 4
    elif key == ord('6'):
        feed = 5
    elif key == ord('w'):
        blockSize += 2
        print (blockSize)
    elif key == ord('s'):
        blockSize -=2
        print (blockSize)
    elif key == ord('d'):
        C += 1
        print (C)
    elif key == ord('a'):
        C -=1
        print (C)
    elif key == ord('j'):
        kern += 1
        print (kern)
    elif key == ord('k'):
        kern -= 1
        print (kern)

#print (img)
#matrix = BWToBoolean(img)
#print (matrix)
#grid = ArrayToGrid(matrix, 4)
#print (grid)
#img = GridToImage(grid)
#cv2.imshow('frame',img)

blocksize = 12
mat = ImageBlocky(img,blocksize)
goodMoves = ImageToBlackList(mat)
path = planPath((0,0),goodMoves,[],len(mat),len(mat[0]))
for i in range(len(path)):
    (x, y) = path[i]
    img[x*blocksize-1][y*blocksize-1] = 0
cv2.imshow('path', img)
while (True):
    if cv2.waitKey(1) & 0xFF == ord('p'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
