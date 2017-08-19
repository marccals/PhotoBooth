import RPi.GPIO as GPIO
import time


class InputButton:
    """Helper class for detect input buttons"""

    def __init__(self, GPIO_channel):

        self.__GPIO_channel = GPIO_channel

        self.__setup_GPIO_channel()
        self.__waiting_for_input = False

        return

    def __del__(self):
        """Clean up GPIO in destructor to gracefully shutdown"""
        GPIO.cleanup()

    def __setup_GPIO_channel(self):
        """Setup GPIO channel"""

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__GPIO_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def wait_for_event(self, callback_event):
        GPIO.add_event_detect(self.__GPIO_channel, GPIO.FALLING)
        GPIO.add_event_callback(self.__GPIO_channel, callback_event)

    def cancel_wait_for_event(self):
        GPIO.remove_event_detect(self.__GPIO_channel)

    def wait_for_input(self):
        try:
            if (not self.__waiting_for_input):
                GPIO.add_event_detect(self.__GPIO_channel, GPIO.FALLING, bouncetime=500)
                self.__waiting_for_input = True

            while True:
                time.sleep(0.1)
                if (GPIO.event_detected(self.__GPIO_channel)):
                    break;
        except KeyboardInterrupt:
            raise
