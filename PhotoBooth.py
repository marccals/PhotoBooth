from BlinkingLed import BlinkingLed
from InputButton import InputButton
from Camera import Camera
from PhotoPathUtils import PhotoPathUtils

import subprocess


cancel_print_button_pressed = False

def cancel_print():
    global cancel_print_button_pressed

    picam.cancel_countdown()
    cancel_print_button_pressed = True

def composed_and_print_captured_image(photo_path):
    composed_photo_path = PhotoPathUtils.get_composed_photo_path(photo_path)

    print ("./ComposeAndPrint.sh " + photo_path + " " + composed_photo_path)

    subprocess.Popen('./ComposeAndPrint.sh ' + photo_path + ' ' + composed_photo_path, shell=True)

picam = Camera()

picam.framerate = 25
picam.start_preview()

blinking_led_capture_button = BlinkingLed(18, 0.5)
blinking_led_cancel_print_button = BlinkingLed(7, 0.5)
blinking_led_cancel_print_button.start(run_in_parallel = True)

input_capture_button = InputButton(4)
input_cancel_print_button = InputButton(11)

blinking_led_capture_button.start(run_in_parallel = True)

input_capture_button.wait_for_input()
#input_cancel_print_button.wait_for_input()

blinking_led_capture_button.stop()

photo_path = PhotoPathUtils.get_photo_path()
picam.capture(photo_path)

input_cancel_print_button.wait_for_event(cancel_print)

picam.preview_captured_image_and_wait_for_print_cancel(5)

input_cancel_print_button.cancel_wait_for_event()
blinking_led_cancel_print_button.stop()

if (not cancel_print_button_pressed):
    composed_and_print_captured_image(photo_path)

picam.stop_preview()



