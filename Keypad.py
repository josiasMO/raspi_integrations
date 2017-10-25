import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

MATRIX = [[1, 2, 3, 'A'],
          [4, 5, 6, 'B'],
          [7, 8, 9, 'C'],
          ['*', 0, '#', 'D']]

ROW = [19, 13, 6, 5]  # Inputs of the keypad
COL = [22, 27, 17, 4]  # Outputs of the keypad


class Keypad(object):
    """   """
    def __init__(self):
        for j in range(4):
            GPIO.setup(COL[j], GPIO.OUT)
            GPIO.output(COL[j], 1)

        for i in range(4):
            GPIO.setup(ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def read_key(self):
        num = 1
        try:
            pressed_key = ""
            while (num>0):
                for j in range(4):
                    GPIO.output(COL[j], 0)

                    for i in range(4):
                        if GPIO.input(ROW[i]) == 0:

                            pressed_key = str(MATRIX[i][j])  # append the key pressed on the keypad
                            num -= 1
                            while (GPIO.input(ROW[i]) == 0):
                                pass

                    GPIO.output(COL[j], 1)

            return pressed_key

        except KeyboardInterrupt:
            GPIO.cleanup()


if __name__ == "__main__":

    keypad = Keypad()

    while True:
        print(keypad.read_key())

