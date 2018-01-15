import cv2
import numpy as np
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(1)

feed = 0

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
            cv2.THRESH_BINARY,11,2)
    elif feed == 3:
        img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,11,2)
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

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
