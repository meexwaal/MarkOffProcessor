import cv2
import numpy as np
from image_processing import *
from path_planning import *

cap = cv2.VideoCapture(1)

ret, frame = cap.read()

fgbg = cv2.createBackgroundSubtractorMOG2(500,64,False)

initialKernel = 5
feed = 6
blockSize = 11
C = 2
kern = 3
blurKernel = 5
masking = False
mask = None
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(kern,kern))
maskcount = 0
maskframes = 60

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    img = frame

    if feed < 7:
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img = cv2.medianBlur(img,initialKernel)

    if feed == 1:
        ret,img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    elif feed == 2:
        img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,blockSize,C)
    elif feed >= 3 and feed < 7:
        img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,blockSize,C)

    if feed == 4:
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    elif feed == 5:
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    elif feed == 6:
        img = cv2.medianBlur(img, blurKernel)
    elif feed == 7:
        fgbg.apply(frame)
        fgbg.getBackgroundImage(img)
    elif feed == 8:
        fgbg.apply(frame)
        fgbg.getBackgroundImage(img)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img = cv2.medianBlur(img,blurKernel)
        img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,11,2)
        img = cv2.medianBlur(img,blurKernel)

    if masking:
        if maskcount < maskframes:
            maskcount = maskcount + 1
            mask = cv2.bitwise_and(img, mask)
        if maskcount == maskframes:
            mask = cv2.erode(mask,kernel)
            maskcount = maskcount + 1
            blurKernel = 3
        img = cv2.bitwise_or(img, cv2.bitwise_not(mask))
        cv2.imshow('mask',mask)

    img = cv2.medianBlur(img,blurKernel)

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
    elif key == ord('9'):
        feed = 8
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
    elif key == ord('m'):
        if masking:
            masking = False
            blurKernel = 5
        else:
            masking = True
            maskcount = 0
            mask = img

#print (img)
#matrix = BWToBoolean(img)
#print (matrix)
#grid = ArrayToGrid(matrix, 4)
#print (grid)
#img = GridToImage(grid)
#cv2.imshow('frame',img)

blocksize = 8
mat = ImageBlocky(img,blocksize)
goodMoves = ImageToBlackList(mat)
badMoves = None
if masking:
    badMoves = ImageToBlackList(ImageBlocky(mask,blocksize))
goodMoves = [i for i in goodMoves if i not in badMoves]
print(goodMoves)
print("================================================")
print(badMoves)
print("================================================")
img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
for g in goodMoves:
    (x,y)=g
    x = x*blocksize-1
    y = y*blocksize-1
    g=(y,x)
    cv2.line(img,g,g,(0,255,0))
for b in badMoves:
    (x,y)=b
    x = x*blocksize-1
    y = y*blocksize-1
    b=(y,x)
    cv2.line(img,b,b,(0,0,255))
cv2.imshow('moves',img)
while (True):
    if cv2.waitKey(1) & 0xFF == ord('p'):
        break
path = planPath((30,60),goodMoves,badMoves,len(mat),len(mat[0]))
lastx, lasty = None, None
for i in range(len(path)):
    (x, y) = path[i]
    x = x*blocksize-1
    y = y*blocksize-1
    img[x][y] = (255,0,0)
    if i > 0:
        cv2.line(img,(lasty,lastx),(y,x),(0,255,0)if i==1 else(255,0,0))
            #cv2.cvtColor(np.array([180 * i / len(path),255,255],dtype=np.uint8),cv2.COLOR_HSV2BGR))
    lastx, lasty = x, y
cv2.imshow('path', img)
while (True):
    if cv2.waitKey(1) & 0xFF == ord('p'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
