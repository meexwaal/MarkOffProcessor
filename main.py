import cv2
import numpy as np
from image_processing import *
from path_planning import *
from robot import *

def main():
    cap = cV2.VideoCapture(1)
    fgbg = cv2.createBackgroundSubtractorMOG2(500,64,False)

    bot = robot()

    while(True):
        ret,frame = cap.read()
        fgbg.apply(frame)

        img = processImage(frame)

        botLoc = findRobot(frame)
        if botLoc == None:
            continue
        update(bot, botLoc)

        path = findPath(img,botLoc)

        setPath(bot, path)


if __name__=="__main__":
    main()
