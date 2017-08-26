from BlinkingLed import BlinkingLed
from InputButton import InputButton
from Camera import Camera
from PhotoPathUtils import PhotoPathUtils

import subprocess
import os
import signal

compose_and_print_process = None

def cancel_print(bin_var):
    global compose_and_print_process
    #Detected some electronical devices generated interferences causing falses positives. Due to this fact, we check that really button has been pressed
    #before cancel print
    if (input_cancel_print_button.check_button_is_pressed()):
        os.killpg(os.getpgid(compose_and_print_process.pid), signal.SIGTERM)
        picam.cancel_countdown()

def composed_and_print_captured_image(photo_path):
    global compose_and_print_process
    composed_photo_path = PhotoPathUtils.get_composed_photo_path(photo_path)

    compose_and_print_process = subprocess.Popen('./ComposeAndPrint.sh ' + photo_path + ' ' + composed_photo_path, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)


CAPTURE_BUTTON_CHANNEL = 4
CANCEL_PRINT_BUTTON_CHANNEL = 11
LED_CAPTURE_BUTTON_CHANNEL = 18
LED_CANCEL_PRINT_BUTTON_CHANNEL = 7

picam = Camera()

picam.framerate = 25
picam.start_preview()

blinking_led_capture_button = BlinkingLed(LED_CAPTURE_BUTTON_CHANNEL, 0.5)
blinking_led_cancel_print_button = BlinkingLed(LED_CANCEL_PRINT_BUTTON_CHANNEL, 0.5)

input_capture_button = InputButton(CAPTURE_BUTTON_CHANNEL)
input_cancel_print_button = InputButton(CANCEL_PRINT_BUTTON_CHANNEL)

try:

    while (True):
        blinking_led_capture_button.start(run_in_parallel = True)
        input_capture_button.wait_for_input()
        blinking_led_capture_button.stop()

        photo_path = PhotoPathUtils.get_photo_path()
        picam.capture(photo_path)
        composed_and_print_captured_image(photo_path)

        blinking_led_cancel_print_button.start(run_in_parallel = True)
        input_cancel_print_button.wait_for_event(cancel_print)
        picam.preview_captured_image_and_wait_for_print_cancel(5)

        input_cancel_print_button.cancel_wait_for_event()
        blinking_led_cancel_print_button.stop()

except KeyboardInterrupt:
    input_cancel_print_button.cancel_wait_for_event()
    blinking_led_cancel_print_button.stop()
    blinking_led_capture_button.stop()

picam.stop_preview()

