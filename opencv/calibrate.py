# Program to select the rectangular board.

import numpy as np
import cv2

WIN_WIDTH, WIN_HEIGHT = 640, 480
COORD_WIDTH, COORD_HEIGHT = 100, 70
refpt = []

cap = cv2.VideoCapture(0)

# ???
class Vector(object):
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def norm(self):
        return (self.x**2 + self.y**2) ** 0.5

    def normalize(self):
        n = Vector.norm(self)
        self.x /= n
        self.y /= n

    def dot(self, other):
        return self.x*other.x + self.y+other.y

    def __repr__(self):
        return "Vector({}, {})".format(self.x, self.y)



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

# https://math.stackexchange.com/q/13404 ???
# ?????????????????
def map_persp(px, py, refpt, new_width=COORD_WIDTH, new_height=COORD_HEIGHT):
    P = Vector(px, py)
    P0 = Vector(refpt[0][0], refpt[0][1])
    P1 = Vector(refpt[1][0], refpt[1][1])
    P2 = Vector(refpt[2][0], refpt[2][1])
    P3 = Vector(refpt[3][0], refpt[3][1])

    L03 = P3 - P0
    L32 = P2 - P3
    L01 = P1 - P0
    L12 = P2 - P1

    N0 = Vector(-L03.y, L03.x); N0.normalize()
    N1 = Vector(L01.y, -L01.x); N1.normalize()
    N2 = Vector(L12.y, -L12.x); N2.normalize()
    N3 = Vector(-L32.y, L32.x); N3.normalize()
    print(N0, N1, N2, N3)
    print(P-P0, P-P1, P-P2, P-P3)

    dU0 = (P - P0).dot(N0)
    dU1 = (P - P2).dot(N2)
    dV0 = (P - P0).dot(N1)
    dV1 = -((P - P3).dot(N3))

    print(dU0, dU1, dV0, dV1)

    u = dU0 / (dU0 + dU1)
    v = dV0 / (dV0 + dV1)

    return u, v


def click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(refpt) < 4:
            print(x, y)
            refpt.append((x,y))
        else:
            print(x, y, map_persp(x, y, refpt))


cv2.namedWindow("frame")
cv2.setMouseCallback("frame", click)

print("Program to select rectangular board.")
print("Start at left bottom corner and go COUNTERclockwise.")

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
