import time

from picamera import PiCamera
from PIL import Image
import numpy as np

class Camera:
    def __init__(self):
        self.__cancel_countdown = False
        self.__picamera = PiCamera()
        self.__counter_pad = {
            5: self.__get_image_pad(self.__get_countdown_image_path(5)),
            4: self.__get_image_pad(self.__get_countdown_image_path(4)),
            3: self.__get_image_pad(self.__get_countdown_image_path(3)),
            2: self.__get_image_pad(self.__get_countdown_image_path(2)),
            1: self.__get_image_pad(self.__get_countdown_image_path(1))
        }

    def __del__(self):
        self.__picamera.close()

    def set_frame_Rate(self, frame_rate):
        self.__picamera.framerate = frame_rate

    def start_preview(self):
        self.__picamera.framerate = 25
        self.__picamera.resolution = (1024, 768)
        self.__picamera.start_preview()

    def stop_preview(self):
        self.__picamera.stop_preview()

    def capture(self, path):
        self.__cancel_countdown = False
        self.startCountDown(3)

        self.__picamera.capture(path)

    def startCountDown(self, seconds):

        for i in xrange(seconds, 0, -1):
            pad = self.__counter_pad
            o = self.__picamera.add_overlay(self.__counter_pad[i].tostring())
            o.layer = 40
            time.sleep(0.9) #0.9
            self.__picamera.remove_overlay(o)
            time.sleep(0.1)
            if (self.__cancel_countdown):
                break;

    def __get_countdown_image_path(self, number):

        switcher = {
            1: "images/NumberOne.png",
            2: "images/NumberTwo.png",
            3: "images/NumberThree.png",
            4: "images/NumberFour.png",
            5: "images/NumberFive.png",
        }

        return switcher.get(number)

    def cancel_countdown(self):
        self.__cancel_countdown = True

    def preview_captured_image_and_wait_for_print_cancel(self, seconds):

        pad = self.__get_image_pad('test.png')

        o = self.__picamera.add_overlay(pad.tostring())
        o.layer = 3

        self.startCountDown(seconds)
        self.__picamera.remove_overlay(o)

    def __get_image_pad(self, path_image):
        # Load the arbitrarily sized image
        img = Image.open(path_image)
        # Create an image padded to the required size with
        # mode 'RGB'

        pad = Image.new('RGBA', (
            ((img.size[0]) // 16) * 16,
            ((img.size[1]) // 32) * 32,
        ))
        # Paste the original image into the padded one
        pad.paste(img, (0, 0), img)

        return pad

        # Add the overlay with the padded image as the source,
        # but the original image's dimensions

        # By default, the overlay is in layer 0, beneath the
        # preview (which defaults to layer 2). Here we make
        # the new overlay semi-transparent, then move it above
        # the preview


