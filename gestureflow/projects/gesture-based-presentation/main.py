from display import DisplayManager
from threading import Thread
from settings import *
from gestureflow.tracker import HandTracker
from gestureflow.sample_gesture_trackers import GestureTracker2D
from gestureflow.sample_state_trackers import RotationCounter, PositionTracker
from gestureflow.sample_runners import Runner
from gestureflow.definitions import *
from state_trackers import *
from gesture_trackers import TwoHandTracker

SLIDE_CHANGE_GESTURE = [True, True, False, False, True]
SLIDE_CHANGE_GESTURE = [True, True, True, False, False]
POINTER_GESTURE = [False, True, False, False, False]
ANNOTATION_GESTURE = [False, True, True, False, False]
ERASER_GESTURE = [True, True, True, True, True]


RIGHT_HAND_GESTURE = [False, True, True, True, False]

SLIDE_CHANGE_LEFT_HAND_GESTURE = [True, True, True, True, True]
POINTER_SIZE_LEFT_HAND_GESTURE = [False, True, True, True, True]
ERASER_SIZE_LEFT_HAND_GESTURE = [False, True, True, True, False]


if __name__ == "__main__":
    state = DEFAULT_STATE_DICT

    handTracker = HandTracker()

    gesture1 = GestureTracker2D()
    gesture2 = GestureTracker2D()
    gesture3 = GestureTracker2D()
    gesture4 = GestureTracker2D()

    gesture1.setTrackLefttHand(False)
    gesture2.setTrackLefttHand(False)
    gesture3.setTrackLefttHand(False)
    gesture4.setTrackLefttHand(False)

    two_hand_gesture1 = TwoHandTracker()
    two_hand_gesture2 = TwoHandTracker()
    two_hand_gesture3 = TwoHandTracker()

    displayManager = DisplayManager()

    slideNumber = RotationCounter()
    pointer = PositionTracker()

    annotation = AnnotationTracker(displayManager)
    eraser = EraserTracker(displayManager)
    slide_tracker = SlideChangeTracker(displayManager)
    pointer_size_tracker = SizeChangeTracker(displayManager)
    eraser_size_tracker = EraserSizeChangeTracker(displayManager)

    runner = Runner()

    slideNumber.setMin(0)
    slideNumber.setMax(10)
    slideNumber.setDiscUnit(30)

    def set_slide_number(slideNo):
        slideNo = int(slideNo)
        displayManager.setSlideNumber(slideNo)

    def show_pointer(coords):
        displayManager.show_pointer(coords[1])

    def annotate(coords):
        displayManager.annotate(coords[1])

    # gesture1.addGesture(SLIDE_CHANGE_GESTURE)
    gesture2.addGesture(POINTER_GESTURE)
    gesture3.addGesture(ANNOTATION_GESTURE)
    gesture4.addGesture(ERASER_GESTURE)

    two_hand_gesture1.set_left_gesture(SLIDE_CHANGE_LEFT_HAND_GESTURE)
    two_hand_gesture1.set_right_gesture(RIGHT_HAND_GESTURE)

    two_hand_gesture2.set_left_gesture(POINTER_SIZE_LEFT_HAND_GESTURE)
    two_hand_gesture2.set_right_gesture(RIGHT_HAND_GESTURE)

    two_hand_gesture3.set_left_gesture(ERASER_SIZE_LEFT_HAND_GESTURE)
    two_hand_gesture3.set_right_gesture(RIGHT_HAND_GESTURE)

    gesture1.addStateTracker(slideNumber)
    gesture2.addStateTracker(pointer)
    gesture3.addStateTracker(annotation)
    gesture4.addStateTracker(eraser)

    two_hand_gesture1.addStateTracker(slide_tracker)
    two_hand_gesture2.addStateTracker(pointer_size_tracker)
    two_hand_gesture3.addStateTracker(eraser_size_tracker)

    handTracker.add_gesture(gesture1)
    handTracker.add_gesture(gesture2)
    handTracker.add_gesture(gesture3)
    handTracker.add_gesture(gesture4)

    handTracker.add_gesture(two_hand_gesture1)
    handTracker.add_gesture(two_hand_gesture2)
    handTracker.add_gesture(two_hand_gesture3)

    slideNumber.setOnUpdate(set_slide_number)
    pointer.setOnUpdate(show_pointer)

    # displayManager.load_from_pptx('test2.pptx')
    displayManager.load_folder('test')

    trackerThread = Thread(target=runner.loop, args=[handTracker])

    trackerThread.start()

    displayManager.runLoop()
