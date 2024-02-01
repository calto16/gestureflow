from gestureflow.sample_gesture_trackers import GestureTracker
from gestureflow.definitions import *
from definitions import *


class TwoHandTracker(GestureTracker):
    def __init__(self) -> None:
        super().__init__()
        self.right_point = None
        self.leftGesture = []
        self.rightGesture = []
        self.right_point = None

    def set_left_gesture(self, gesture):
        self.leftGesture = gesture

    def set_right_gesture(self, gesture):
        self.rightGesture = gesture

    def updateState(self, leftHandState, rightHandState):
        x, y = rightHandState[COORD_LIST][8]
        self.right_point = (x, y)
        self.gestureFound = True

    def track(self, handStates):
        leftHandState = None
        rightHandState = None
        for handState in handStates:
            if handState[HAND_LABEL] == 'Left':
                leftHandState = handState
            else:
                rightHandState = handState

        if leftHandState and rightHandState and (
                leftHandState[FINGERS_UP] == self.leftGesture) and (
                    rightHandState[FINGERS_UP] == self.rightGesture):
            self.updateState(leftHandState, rightHandState)
        else:
            self.gestureFound = False
            self.resetState()

        for stateTracker in self.stateTrackers:
            stateTracker.update(self.getState())

    def getState(self):
        return {
            GESTURE_FOUND: self.gestureFound,
            ANGLE_Z: self.angleZ,
            HAND_CENTER: self.center,
            FINGER_POINTS: self.fingerPoints,
            RIGHT_POINT: self.right_point
        }
