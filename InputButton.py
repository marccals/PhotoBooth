import RPi.GPIO as GPIO


class InputButton:
    """Helper class for detect input buttons"""

    def __init__(self, GPIO_channel):

        self.__GPIO_channel = GPIO_channel

        self.__setup_GPIO_channel()

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
        GPIO.wait_for_edge(self.__GPIO_channel, GPIO.FALLING)
