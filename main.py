import cv2
import numpy as np
from image_processing import *
from path_planning import *
from robot import *
import tracking


def main():
    cap = cv2.VideoCapture(0)

    # mask
    while(True):
      ret,frame = cap.read()
      if frame is None:
        print("frame is None")
        continue
      img = processImage(frame)
      cv2.imshow('Image',img)
      key = cv2.waitKey(1) & 0xFF
      if doneBuilding():
        if key == ord('m'):
          toggleMask(img)
        if key == ord('p'):
          break
    
    print("made mask")
    print("searching for bot...")
        
    # plan
    botLoc = None
    while(botLoc is None):
      ret,frame = cap.read()
      botLoc = tracking.track(frame)

    print("found bot at", botLoc)
    print("initializing bot...")
    bot = robot(botLoc)
    print("initialized bot!")

    print("finding path...")
    ret,frame = cap.read()
    img = processImage(frame)
    path = findPath(img,botLoc)
    print("found it")
    
    bot.followLine(path)

    # move
    while(True):
        ret,frame = cap.read()

        img = processImage(frame)

        botLoc = tracking.track(frame)
        print("bot location:", botLoc)
        
        if botLoc == None:
            continue
        
        bot.update(botLoc)

if __name__=="__main__":
    main()
