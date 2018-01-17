import cv2
import numpy as np
from matplotlib import pyplot as plt
from image_processing import *
from path_planning import *

cap = cv2.VideoCapture(1)

fgbg = cv2.createBackgroundSubtractorMOG2(500,64,False)

initialKernel = 5
feed = 7
blockSize = 11
C = 2
kern = 5
blurKernel = 5

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    img = frame

    if feed != 7:
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img = cv2.medianBlur(img,initialKernel)

    if feed == 1:
        ret,img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    elif feed == 2:
        img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,blockSize,C)
    elif feed >= 3 and feed != 7:
        img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,blockSize,C)

    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(kern,kern))
    if feed == 4:
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    elif feed == 5:
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    elif feed == 6:
        img = cv2.medianBlur(img, blurKernel)
    elif feed == 7:
        fgbg.apply(frame)
        fgbg.getBackgroundImage(img)

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
    elif key == ord('7'):
        feed = 6
    elif key == ord('8'):
        feed = 7
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
    elif key == ord('h'):
        blurKernel -= 2
        print(blurKernel)
    elif key == ord('l'):
        blurKernel += 2
        print(blurKernel)
    elif key == ord('f'):
        initialKernel -= 2
        print(initialKernel)
    elif key == ord('g'):
        initialKernel += 2
        print(initialKernel)

#print (img)
#matrix = BWToBoolean(img)
#print (matrix)
#grid = ArrayToGrid(matrix, 4)
#print (grid)
#img = GridToImage(grid)
#cv2.imshow('frame',img)

blocksize = 11
mat = ImageBlocky(img,blocksize)
goodMoves = ImageToBlackList(mat)
path = planPath((0,0),goodMoves,[],len(mat),len(mat[0]))
img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
lastx, lasty = None, None
for i in range(len(path)):
    (x, y) = path[i]
    x = x*blocksize-1
    y = y*blocksize-1
    img[x][y] = (255,0,0)
    if i > 0:
        cv2.line(img,(lasty,lastx),(y,x),(255,0,0))
            #cv2.cvtColor(np.array([180 * i / len(path),255,255],dtype=np.uint8),cv2.COLOR_HSV2BGR))
    lastx, lasty = x, y
cv2.imshow('path', img)
while (True):
    if cv2.waitKey(1) & 0xFF == ord('p'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
