"""Buzzer Module"""

# !/usr/bin/env python
import RPi.GPIO as GPIO
from time import sleep

BUZZERPIN = 26  # Raspberry Pi Pin 17-GPIO 17

class Buzzer():
    """Sound generator using buzzer"""
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)  # Set GPIO Pin As Numbering
        GPIO.setup(BUZZERPIN, GPIO.OUT)
        GPIO.output(BUZZERPIN, GPIO.LOW)

    def on(self):
        GPIO.output(BUZZERPIN, GPIO.HIGH)

    def off(self):
        GPIO.output(BUZZERPIN, GPIO.LOW)


    def beep(self, type):
        """Types: confirm, cancel, welcome, start_journey end_journey, number, wrong_key"""

        if type == "confirm":
            self.on()
            sleep(0.1)
            self.off()
            sleep(0.1)
            self.on()
            sleep(0.1)
            self.off()

        elif type == "cancel":
            self.on()
            sleep(0.4)
            self.off()
            sleep(0.1)
            self.on()
            sleep(0.1)
            self.off()

        elif type == "welcome":
            self.on()
            sleep(0.2)
            self.off()
            sleep(0.5)

            self.on()
            sleep(0.2)
            self.off()
            sleep(0.1)

            self.on()
            sleep(0.2)
            self.off()
            sleep(0.5)

            self.on()
            sleep(0.3)
            self.off()
            sleep(0.25)

        elif type == "start_journey":
            self.on()
            sleep(0.05)
            self.off()
            sleep(0.05)
            self.on()
            sleep(0.05)
            self.off()
            sleep(0.1)
            self.on()
            sleep(0.05)
            self.off()
            sleep(0.05)
            self.on()
            sleep(0.05)
            self.off()

        elif type == "end_journey":
            self.on()
            sleep(0.02)
            self.off()
            sleep(0.02)
            self.on()
            sleep(0.02)
            self.off()
            sleep(0.1)
            self.on()
            sleep(0.02)
            self.off()
            sleep(0.02)
            self.on()
            sleep(0.02)
            self.off()

        elif type == "number":
            self.on()
            sleep(0.05)
            self.off()

        elif type == "wrong_key":
            self.on()
            sleep(0.5)
            self.off()

    def destroy(self):
        GPIO.output(BUZZERPIN, GPIO.HIGH)
        GPIO.cleanup()  # Release resource



# if __name__ == '__main__':  # Program start from here
#     buzzer = Buzzer()
# try:
#     buzzer.beep("confirm")
#     sleep(3)
#     buzzer.beep("cancel")
# except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be executed.
#     buzzer.destroy()