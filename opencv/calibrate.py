# Program to select the rectangular board.

import numpy as np
import cv2

WIN_WIDTH, WIN_HEIGHT = 640, 480
COORD_WIDTH, COORD_HEIGHT = 100, 70
refpt = []

cap = cv2.VideoCapture(1)


# https://math.stackexchange.com/q/`3404 ???
# mystery ugly trapezoid to rectangle functionq
def approx_persp(px, py, new_width=COORD_WIDTH, new_height=COORD_HEIGHT):
    scaley = (py - refpt[1][1]) / (refpt[0][1]-refpt[1][1])
    wx = refpt[1][0] - scaley * (refpt[1][0]-refpt[0][0])
    dx12 = refpt[2][0] - refpt[1][0]
    dx03 = refpt[3][0] - refpt[0][0]
    horiz = dx12 + scaley * (dx03 - dx12)
    scalex = (px - wx) / horiz

    newx = scalex * new_width
    newy = scaley * new_height
    return newx, newy


def click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(refpt) < 4:
            print(x, y)
            refpt.append((x,y))
        else:
            print(x, y, approx_persp(x, y))


cv2.namedWindow("frame")
cv2.setMouseCallback("frame", click)

print("Program to select rectangular board.")
print("Start at left bottom corner and go clockwise.")

YELLOW = (0, 255, 255)
HORIZ_THRESH = 0.02
file_written = False

while(True):
    ret, frame = cap.read()

    # Draw rectangle
    if len(refpt) >= 2:
        cv2.line(frame, refpt[0], refpt[1], YELLOW, 10)
    if len(refpt) >= 3:
        cv2.line(frame, refpt[1], refpt[2], YELLOW, 10)
    if len(refpt) >= 4:
        cv2.line(frame, refpt[2], refpt[3], YELLOW, 10)
        cv2.line(frame, refpt[3], refpt[0], YELLOW, 10)

    cv2.imshow('frame', frame)

    if len(refpt) == 4 and not file_written:
        m12 = (refpt[1][1] - refpt[2][1]) / (refpt[1][0] - refpt[2][0])
        m03 = (refpt[0][1] - refpt[3][1]) / (refpt[0][0] - refpt[3][0])

        if m12 > HORIZ_THRESH or m03 > HORIZ_THRESH:
            print("WARNING: Board view may not be horizontal!")
            print("Robot may not end up where you think!")

        print("Writing file...")
        with open("refpt.txt", 'w') as f:
            for i in range(4):
                f.write("{} {}\n".format(refpt[i][0], refpt[i][1]))

        file_written = True


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break




cap.release()
cv2.destroyAllWindows()
