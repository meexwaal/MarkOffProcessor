import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

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

        # Draw centroid
        cv2.circle(frame, (cx, cy), 10, (255, 0, 0), -1)

        print(M["m00"]/255, cx, cy)


    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
