import cv2
import numpy as np
from image_processing import *
from path_planning import *
from robot import *


def main():
    cap = cv2.VideoCapture(-1)

    #bot = robot()

    # mask
    while(True):
      ret,frame = cap.read()
      if frame is None:
        print("frame is None")
        #continue
      img = processImage(frame)
      cv2.imshow('Image',img)
      key = cv2.waitKey(1) & 0xFF
      if doneBuilding():
        if key == ord('m'):
          toggleMask(img)
        if key == ord('p'):
          break
    
    # plan
    botLoc = None
    while(botLoc is None):
      ret,frame = cap.read()
      botloc = findRobot(frame)

    ret,frame = cap.read()
    img = processImage(frame)
    path = findPath(img,botLoc)
    bot.followLine(path)

    # move
    while(True):
        ret,frame = cap.read()

        img = processImage(frame)

        botLoc = findRobot(frame)
        if botLoc == None:
            continue
        bot.update(botLoc)

if __name__=="__main__":
    main()
