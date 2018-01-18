from distance import distance
from pathSmooth import pathSmooth
import PID
from enum import Enum
import wrapper
from numpy import clip, binary_repr

ROTATION_SCALE = 190
ROTATION_MID = 465

class robot:

    # Number of points from the path to consider for distance
    # (to keep the bot from getting confused)
    numPathPts = 20
    MAX_CLOSE_TO_POINT = .3;

    # PID to do line following
    linePID = PID.PID()

    # PID to do rotating to an angle
    rotPID = PID.PID()

    # Class to do the bluetooth
    bt = wrapper.bt()

    class Mode(Enum):
        STILL = 0
        ROTATING = 1
        LINE_FOLLOW = 2

    ### Fields:
    # pos : (real,real) - the position of the bot on the grid
    # rot : (real,real) - the orientation of bot as XY accelerations (scaled to -1 to 1)
    # path : (real,real) array - the list of points on the path
    # rotTarget : real - angle to rotate to
    # mode : mode_enum - what the current mode should be
    # lineSpeed : real - result of linePID, which is like angular speed
    # angSpeed : real - result of rotPID, which is actually angular speed
    # motor : (real,real) - the values to drive the motor (-1 to 1 for each motor)

    def __init__(self, pos = None, rot=None, path=None, rotTarget=None,
                 mode=Mode.STILL):
        self.pos = pos
        self.rot = rot
        self.path = path
        self.rotTarget = rotTarget
        self.mode = mode

        self.lineSpeed = 0
        self.angSpeed = 0
        self.motor = (0,0)

        self.start_point_index = 0

    def setPos(self, pos):
        self.pos = pos
    def setPath(self, path):
        self.path = path

    # update should be called at a regular interval
    # (derivative should be wrt time, so needs a constant delta-T)
    def update(self, pos):
        self.pos = pos
        if rot != None:
            self.rot = rot

        if self.mode == self.Mode.LINE_FOLLOW:
            self.lineSpeed = self.linePID.update(self.getDistance())
        elif self.mode == self.Mode.ROTATING:
            self.angSpeed = self.rotPID.update(self.anglify(self.rot))

        self.updateRot()
        self.updateMotors()

    def updateRot(self):
        inp = bt.read_last()
        if inp != None:
            self.rot = ((inp[0] - ROTATION_MIDDLE)/ROTATION_SCALE,
                        (inp[1] - ROTATION_MIDDLE)/ROTATION_SCALE)

    def changeMode(self, newMode):
        self.mode = newMode
        if newMode == self.Mode.LINE_FOLLOW:
            self.linePID.setPoint(0)
        elif newMode == self.Mode.ROTATING:
            self.rotPID.setPoint(self.rotTarget)


    # Return (Lspeed,Rspeed) based on the current mode
    def getMotors(self):
        # TODO: make the numbers actually make sense
        if self.mode == self.Mode.STILL:
            res = (0,0)
        elif self.mode == self.Mode.ROTATING:
            res = (angSpeed, -angSpeed)
        elif self.mode == self.Mode.LINE_FOLLOW:
            res = (0.1+self.lineSpeed, 0.1-self.lineSpeed) # or something like that
        else:
            print("[ERROR] literally the mode isn't a mode")
            return None

        return (clip(res[0],-1,1), clip(res[1],-1,1))

    def updateMotors(self):
        lm, rm = self.getMotors()
        lb = binary_repr(int(lm*7.99), width=4) # for DEEP and MEANINGFUL reasons
        rb = binary_repr(int(rm*7.99), width=4)
        self.bt.write(int(lb+rb, 2))
        
    def smoothPath(self):
        self.path = pathSmooth(self.path)


    def followLine(self, path=None):
        if path != None:
            self.setPath(path)
        self.changeMode(self.Mode.LINE_FOLLOW)
        
    def rotateTo(self, angle=None):
        if angle != None:
            self.rotTarget = angle
        self.changeMode(self.Mode.ROTATING)

    def stop(self):
        self.changeMode(self.Mode.STILL)

    # getDistance : void -> real
    def getDistance(self):
        cut_path_end_index = min(start_point_index + self.numPathPts,len(self.path))
        if(cut_path_end_index <= start_point_index): self.stop

        cutPath = self.path[start_point_index:cut_path_end_index]

        d,shortest_distance_to_point,shortest_point_index = distance(self.pos, cutPath, self.rot)

        if (shortest_distance_to_point < MAX_CLOSE_TO_POINT 
            and shortest_point_index > 3):
            self.start_point_index += shortest_point_index - 3

        return d


    def anglify(self, rot):
        # TODO
        return 0
