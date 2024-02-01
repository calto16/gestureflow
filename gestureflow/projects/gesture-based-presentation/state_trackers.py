from gestureflow.definitions import *
from definitions import *


class AnnotationTracker():
    def __init__(self, displayManager) -> None:
        self.prev_position = None
        self.displayManager = displayManager

    def update(self, state):
        if state[GESTURE_FOUND]:
            cur_position = tuple(state[FINGER_POINTS][1])
            if self.prev_position:
                self.displayManager.annotate(self.prev_position, cur_position)
            self.prev_position = cur_position
        else:
            self.prev_position = None


class EraserTracker():
    def __init__(self, displayManager) -> None:
        self.prev_position = None
        self.displayManager = displayManager

    def update(self, state):
        if state[GESTURE_FOUND]:
            cur_position = tuple(state[HAND_CENTER])
            self.displayManager.erase_point(cur_position)
            self.prev_position = cur_position
        else:
            self.prev_position = None


class SlideChangeTracker():
    def __init__(self, displayManager) -> None:
        self.prev_position = None
        self.displayManager = displayManager
        self.displacement = 0
        self.slideNumber = 0
        self.slideUnits = 50

        self.max_slide_number = 10
        self.min_slide_number = 0

    def set_min_max(self, min_slide_number, max_slide_number):
        self.max_slide_number = max_slide_number
        self.min_slide_number = min_slide_number

    def update(self, state):
        if state[GESTURE_FOUND]:
            cur_position = state[RIGHT_POINT]
            if self.prev_position:
                self.displacement += cur_position[0] - self.prev_position[0]
                self.displacement = min(self.max_slide_number * self.slideUnits, max(
                    self.min_slide_number * self.slideUnits, self.displacement))
                self.slideNumber = self.displacement // self.slideUnits
                self.displayManager.setSlideNumber(self.slideNumber)
            self.prev_position = cur_position
        else:
            self.prev_position = None


class SizeChangeTracker():
    def __init__(self, displayManager) -> None:
        self.prev_position = None
        self.displayManager = displayManager
        self.pointerSize = 4
        self.pointerSizeUnits = 50
        self.displacement = self.pointerSize * self.pointerSizeUnits

        self.max_pointer_size = 10
        self.min_pointer_size = 1

    def set_min_max(self, min_pointer_size, max_pointer_size):
        self.max_pointer_size = max_pointer_size
        self.min_pointer_size = min_pointer_size

    def update(self, state):
        if state[GESTURE_FOUND]:
            cur_position = state[RIGHT_POINT]
            if self.prev_position:
                self.displacement += cur_position[0] - self.prev_position[0]
                self.displacement = min(self.max_pointer_size * self.pointerSizeUnits, max(
                    self.min_pointer_size * self.pointerSizeUnits, self.displacement))
                self.pointerSize = self.displacement // self.pointerSizeUnits
                self.displayManager.set_pointer_size(self.pointerSize)
            self.prev_position = cur_position
        else:
            self.prev_position = None


class EraserSizeChangeTracker():
    def __init__(self, displayManager) -> None:
        self.prev_position = None
        self.displayManager = displayManager
        self.pointerSize = 8
        self.pointerSizeUnits = 50
        self.displacement = self.pointerSize * self.pointerSizeUnits

        self.max_pointer_size = 30
        self.min_pointer_size = 1

    def set_min_max(self, min_pointer_size, max_pointer_size):
        self.max_pointer_size = max_pointer_size
        self.min_pointer_size = min_pointer_size

    def update(self, state):
        if state[GESTURE_FOUND]:
            cur_position = state[RIGHT_POINT]
            if self.prev_position:
                self.displacement += cur_position[0] - self.prev_position[0]
                self.displacement = min(self.max_pointer_size * self.pointerSizeUnits, max(
                    self.min_pointer_size * self.pointerSizeUnits, self.displacement))
                self.pointerSize = self.displacement // self.pointerSizeUnits
                self.displayManager.set_eraser_size(self.pointerSize)
            self.prev_position = cur_position
        else:
            self.prev_position = None
