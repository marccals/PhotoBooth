import RPi.GPIO as GPIO
import time


class BlinkingLed:
    """Helper class for blinking leds."""

    def __init__(self, GPIO_channel, blinking_time):
        """Minium blinking_time has to be >= 0.1"""

        self.__GPIO_channel = GPIO_channel
        self.__blinking_time = blinking_time

        self.__isBlinking = False
        self.__sleep_time = 0.1

        self.__setup_GPIO_channel()

        return

    def __del__(self):
        """Clean up GPIO in destructor to gracefully shutdown"""
        GPIO.cleanup()

    def __setup_GPIO_channel(self):
        """Setup GPIO channel"""

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.__GPIO_channel, GPIO.OUT)

    def __turn_on_led(self):
        GPIO.output(self.__GPIO_channel, GPIO.HIGH)

    def __turn_off_led(self):
        GPIO.output(self.__GPIO_channel, GPIO.LOW)

    def __toogle_led_state(self):
        if (self.__is_led_on()):
            self.__turn_off_led()
        else:
            self.__turn_on_led()

    def __is_led_on(self):
        """returns boolean indicating if led is on"""
        return GPIO.input(self.__GPIO_channel) == GPIO.HIGH

    def start(self):
        """Start blinking led"""

        time_to_switch_led_state =  self.__blinking_time

        self.__isBlinking = True
        self.__turn_on_led()

        while self.__isBlinking:
            time.sleep(self.__sleep_time)
            time_to_switch_led_state -= self.__sleep_time

            if time_to_switch_led_state <= 0:
                time_to_switch_led_state = self.__blinking_time
                self.__toogle_led_state()

        """Be sure that led always is off before exit"""
        self.__turn_off_led()

    def stop(self):
        """Stop blinking led"""

        self.__isBlinking = False