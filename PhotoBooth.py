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

    os.killpg(os.getpgid(compose_and_print_process.pid), signal.SIGTERM)
    picam.cancel_countdown()


def composed_and_print_captured_image(photo_path):
    global compose_and_print_process
    composed_photo_path = PhotoPathUtils.get_composed_photo_path(photo_path)

    compose_and_print_process = subprocess.Popen('./ComposeAndPrint.sh ' + photo_path + ' ' + composed_photo_path, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)


picam = Camera()

picam.framerate = 25
picam.start_preview()

blinking_led_capture_button = BlinkingLed(18, 0.5)
blinking_led_cancel_print_button = BlinkingLed(7, 0.5)

input_capture_button = InputButton(4)
input_cancel_print_button = InputButton(11)

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

picam.stop_preview()

