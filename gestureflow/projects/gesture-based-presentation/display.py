from spire.presentation import Presentation
import os
from tkinter import Tk, Label
from PIL import Image, ImageTk, ImageDraw
from threading import Thread
import time
from settings import *
import numpy as np
import copy
import cv2

TOOL_BAR_COLOR = (128, 128, 128)


def rectangle_coords(x, y, size):
    return (x - size, y - size, x + size, y + size)


def map_points(x, y):
    x, y = 2 * x - 50, 2 * y - 50
    return (int(x), int(y))


def save_slides_as_png(input_filename, output_foldername):
    image_paths = []
    # Load the PowerPoint presentation
    presentation = Presentation()
    presentation.LoadFromFile(input_filename)

    for i, slide in enumerate(presentation.Slides):
        # Specify the output file name
        fileName = os.path.join(output_foldername, f"slide{i}.png")
        image_paths.append(fileName)
        # Save each slide as a PNG image
        image = slide.SaveAsImage()
        print(f"Loading slide: {i}")
        image.Save(fileName)
        image.Dispose()

    presentation.Dispose()
    return image_paths


class DisplayManager:
    def __init__(self):
        self.title = ""
        self.slides = []
        self.canvas = []
        self.slidePaths = []
        self.slideNumber = 0

        self.pointer_size = 4
        self.pointer_color = (255, 0, 0)

        self.eraser_size = 15
        self.eraser_color = (0, 0, 255)

        self.root = Tk()
        self.image_label = Label(self.root)
        self.image_label.pack()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def erase(self, point1, point2):
        cur_slide = self.canvas[self.slideNumber]
        cv2.line(cur_slide, point1, point2,
                 self.pointer_color, self.pointer_size)
        self.show()

    def show_eraser(self, point):
        cur_slide = self.canvas[self.slideNumber]

        x, y = point
        x, y = map_points(x, y)

        tl_x, tl_y, br_x, br_y = rectangle_coords(x, y, self.eraser_size)
        top_left = (tl_x, tl_y)
        bottom_right = (br_x, br_y)

        tl_x, tl_y = tl_x - 1, tl_y - 1
        br_x, br_y = br_x + 1, br_y + 1

        prev_region = cur_slide[tl_y:br_y, tl_x:br_x].copy()

        cv2.rectangle(cur_slide, top_left, bottom_right,
                      self.eraser_color, thickness=-1)

        self.show()
        cur_slide[tl_y:br_y, tl_x:br_x] = prev_region

    def erase_point(self, point):

        cur_slide = self.canvas[self.slideNumber]

        x, y = point
        x, y = map_points(x, y)

        tl_x, tl_y = x - self.eraser_size, y - self.eraser_size
        br_x, br_y = x + self.eraser_size, y + self.eraser_size
        top_left = (tl_x, tl_y)
        bottom_right = (br_x, br_y)

        tl_x, tl_y = tl_x - 1, tl_y - 1
        br_x, br_y = br_x + 1, br_y + 1

        cv2.rectangle(cur_slide, top_left, bottom_right,
                      self.eraser_color, thickness=-1)

        self.show()

        cur_slide[tl_y:br_y,
                  tl_x:br_x] = self.slides[self.slideNumber][tl_y:br_y, tl_x:br_x].copy()

    def annotate(self, point1, point2):
        cur_slide = self.canvas[self.slideNumber]
        x1, y1 = point1
        x2, y2 = point2
        x1, y1 = x1 * 2, y1 * 2
        x2, y2 = x2 * 2, y2 * 2
        point1 = (x1, y1)
        point2 = (x2, y2)
        cv2.line(cur_slide, point1, point2,
                 self.pointer_color, self.pointer_size)
        self.show()

    def show(self):
        cur_slide = self.canvas[self.slideNumber]
        pil_slide = Image.fromarray(cur_slide)

        photo = ImageTk.PhotoImage(pil_slide)
        self.image_label.config(image=photo)
        self.image_label.image = photo

    def show_pointer(self, coords):
        cur_slide = self.canvas[self.slideNumber]
        x, y = coords
        x, y = map_points(x, y)

        tl_x, tl_y, br_x, br_y = rectangle_coords(x, y, self.pointer_size)

        top_left = (tl_x, tl_y)
        bottom_right = (br_x, br_y)

        tl_x, tl_y = tl_x - 1, tl_y - 1
        br_x, br_y = br_x + 1, br_y + 1

        original_region = cur_slide[tl_y:br_y, tl_x:br_x].copy()

        cv2.rectangle(cur_slide, top_left, bottom_right,
                      self.pointer_color, thickness=-1)

        self.show()

        cur_slide[tl_y:br_y, tl_x:br_x] = original_region

    def nextSlide(self):
        if self.slideNumber == len(self.slides):
            self.slideNumber = 0
        self.show()
        self.slideNumber += 1

    def prevSlide(self):
        if self.slideNumber == len(self.slides):
            self.slideNumber = 0
        self.show()
        self.slideNumber += 1

    def setSlideNumber(self, slideNumber):
        self.slideNumber = max(0, min(slideNumber, len(self.slides) - 1))
        self.show()

    def load_from_pptx(self, input_filename):

        self.title, _ = os.path.splitext(os.path.basename(input_filename))
        self.root.title(self.title)

        output_foldername = os.path.join(IMAGE_PATH, self.title)
        if not os.path.exists(output_foldername):
            os.makedirs(output_foldername)

        self.slidePaths = save_slides_as_png(input_filename, output_foldername)
        self.load_images()
        self.show()

    def load_folder(self, folderName):
        self.title = folderName
        folderPath = os.path.join(IMAGE_PATH, folderName)
        self.root.title(self.title)
        self.slidePaths = [os.path.join(folderPath, fileName)
                           for fileName in os.listdir(folderPath)]
        self.slidePaths.sort()
        self.load_images()
        self.show()

    def load_images(self):
        for path in self.slidePaths:
            slide = cv2.imread(path)
            canvas = copy.deepcopy(slide)
            self.slides.append(slide)
            self.canvas.append(canvas)

    def on_closing(self):
        self.root.destroy()

    def runLoop(self):
        self.root.mainloop()

    def set_pointer_size(self, pointer_size):
        self.pointer_size = pointer_size
        self.show_tools()

    def set_eraser_size(self, eraser_size):
        self.eraser_size = eraser_size
        self.show_tools()

    def show_tools(self):
        cur_slide = self.canvas[self.slideNumber]

        px1, py1, px2, py2 = rectangle_coords(20, 20, self.pointer_size)
        pointer_top_left = (px1, py1)
        pointer_bottom_right = (px2, py2)

        ex1, ey1, ex2, ey2 = rectangle_coords(50, 50, self.eraser_size)
        eraser_top_left = (ex1, ey1)
        eraser_bottom_right = (ex2, ey2)

        top_left = (0, 0)
        bottom_right = (100, 100)
        tl_x, tl_y = top_left
        br_x, br_y = bottom_right

        br_x += 1
        br_y += 1

        original_region = cur_slide[tl_y:br_y, tl_x:br_x].copy()
        cv2.rectangle(cur_slide, top_left, bottom_right,
                      TOOL_BAR_COLOR, thickness=-1)

        cv2.rectangle(cur_slide, pointer_top_left, pointer_bottom_right,
                      self.pointer_color, thickness=-1)
        cv2.rectangle(cur_slide, eraser_top_left, eraser_bottom_right,
                      self.eraser_color, thickness=-1)

        self.show()
        cur_slide[tl_y:br_y, tl_x:br_x] = original_region


def update(displayManager):
    while True:
        displayManager.nextSlide()
        time.sleep(2)


if __name__ == "__main__":
    displayManager = DisplayManager()
    displayManager.load_from_pptx('test.pptx')
    Thread(target=update, args=[displayManager]).start()
    displayManager.root.mainloop()
