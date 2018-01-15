from distance import distance
import PID
from enum import Enum

class robot:

    # Number of points from the path to consider for distance
    # (to keep the bot from getting confused)
    self.numPathPts = 20

    # PID to do line following
    self.linePID = PID.PID()

    # PID to do rotating to an angle
    self.rotPID = PID.PID()

    class Mode(Enum):
        STILL = 0
        ROTATING = 1
        LINE_FOLLOW = 2

    ### Fields:
    # pos : (real,real) - the position of the bot on the grid
    # rot : (real,real) - the orientation of bot as XY accelerations
    # path : (real,real) array - the list of points on the path
    # motor : (int,int) - the values to drive the motor
    # mode : mode_enum - what the current mode should be
    # rotTarget : real - angle to rotate to

    def __init__(self, pos = None, rot=None, path=None):
        self.pos = pos

    def setPos(self, pos):
        self.pos = pos
    def setRot(self, rot):
        self.rot = rot
    def setPath(self, path):
        self.path = path

    # update should be called at a regular interval
    # (derivative should be wrt time, so needs a constant delta-T)
    def update(self, pos, rot):
        self.pos = pos
        self.rot = rot
        if self.mode == Mode.LINE_FOLLOW:
            self.linePID.update(self.getDistance())
        elif self.mode == Mode.ROTATING:
            self.rotPID.update(self.anglify(self.rot))

    def changeMode(self, newMode):
        self.mode = newMode
        if newMode == Mode.LINE_FOLLOW:
            self.linePID.setPoint(0)
        elif newMode == Mode.ROTATING:
            self.rotPID.setPoint(self.rotTarget)

    def followLine(self):
        self.changeMode(Mode.LINE_FOLLOWING)

    def rotateTo(self, angle):
        self.rotTarget = angle
        self.changeMode(Mode.ROTATING)

    # getDistance : void -> real
    def getDistance(self):
        cutPath = (self.path[:self.numPathPts]
                   if self.numPathPts < len(self.path)
                   else self.path)
        return distance(self.pos, cutPath, self.rot)

    def anglify(self, rot):
        # TODO
        return 0
