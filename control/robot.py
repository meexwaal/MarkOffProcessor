from distance import distance
import PID
from enum import Enum

class robot:

    # Number of points from the path to consider for distance
    # (to keep the bot from getting confused)
    numPathPts = 20

    # PID to do line following
    linePID = PID.PID()

    # PID to do rotating to an angle
    rotPID = PID.PID()

    class Mode(Enum):
        STILL = 0
        ROTATING = 1
        LINE_FOLLOW = 2

    ### Fields:
    # pos : (real,real) - the position of the bot on the grid
    # rot : (real,real) - the orientation of bot as XY accelerations
    # path : (real,real) array - the list of points on the path
    # rotTarget : real - angle to rotate to
    # mode : mode_enum - what the current mode should be
    # lineSpeed : real - result of linePID, which is like angular speed
    # angSpeed : real - result of rotPID, which is actually angular speed
    # motor : (int,int) - the values to drive the motor

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

    def setPos(self, pos):
        self.pos = pos
    def setRot(self, rot):
        self.rot = rot
    def setPath(self, path):
        self.path = path

    # update should be called at a regular interval
    # (derivative should be wrt time, so needs a constant delta-T)
    def update(self, pos, rot=None):
        self.pos = pos
        if rot != None:
            self.rot = rot

        if self.mode == self.Mode.LINE_FOLLOW:
            self.lineSpeed = self.linePID.update(self.getDistance())
        elif self.mode == self.Mode.ROTATING:
            self.angSpeed = self.rotPID.update(self.anglify(self.rot))

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
            return (0,0)
        elif self.mode == self.Mode.ROTATING:
            return (angSpeed, -angSpeed)
        elif self.mode == self.Mode.LINE_FOLLOW:
            return (100+self.lineSpeed, 100-self.lineSpeed) # or something like that

    def followLine(self, path=None):
        if path != None:
            self.setPath(path)
        self.changeMode(self.Mode.LINE_FOLLOW)
        #
    def rotateTo(self, angle=None):
        if angle != None:
            self.rotTarget = angle
        self.changeMode(self.Mode.ROTATING)

    def stop(self):
        self.changeMode(self.Mode.STILL)

    # getDistance : void -> real
    def getDistance(self):
        cutPath = (self.path[:self.numPathPts]
                   if self.numPathPts < len(self.path)
                   else self.path)
        return distance(self.pos, cutPath, self.rot)

    def anglify(self, rot):
        # TODO
        return 0
