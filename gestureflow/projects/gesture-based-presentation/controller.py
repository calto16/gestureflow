from settings import *

class Controller:
    def __init__(self, state, displayManager):
        self.state = state
        self.displayManager = displayManager
        self.slideDel = 0
        self.slideNumber = 0

    def run(self):
        slideNumber = self.slideNumber
        rightAngle = self.state[RIGHT_DISC_ANGLE]
        if rightAngle:
            self.slideDel = int(rightAngle // ANGLE_UNIT)
            slideNumber += self.slideDel
        else:
            self.slideNumber += self.slideDel
            self.slideDel = 0
        self.displayManager.setSlideNumber(self.slideNumber + self.slideDel)

    def loop(self):
        while True:
            self.run()
