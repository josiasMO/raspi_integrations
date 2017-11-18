"""Keypad Manipulation Module"""

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

MATRIX = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 9],
          ['ini', 0, 'fim'],
          ['con', 'fun', 'can']]
ROW = [6, 5, 22, 27, 17]  # Inputs of the keypad
COL = [13, 19, 26]  # Outputs of the keypad



class Keypad(object):
    """Keypad class"""
    def __init__(self):
        for j in range(3):
            GPIO.setup(COL[j], GPIO.OUT)
            GPIO.output(COL[j], 1)

        for i in range(5):
            GPIO.setup(ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def read_key(self):
        num = 1
        try:
            pressed_key = ""
            while num > 0:
                for j in range(3):
                    GPIO.output(COL[j], 0)

                    for i in range(5):
                        if GPIO.input(ROW[i]) == 0:

                            pressed_key = str(MATRIX[i][j])  # append the key pressed on the keypad
                            num -= 1
                            while GPIO.input(ROW[i]) == 0:
                                pass

                    GPIO.output(COL[j], 1)

            return pressed_key

        except KeyboardInterrupt:
            GPIO.cleanup()
#
# if __name__ == "__main__":
#     keypad = Keypad()
#     while True:
#         print(keypad.read_key())
