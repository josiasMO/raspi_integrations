""""Python module to manipulate the LCD display"""
import Adafruit_CharLCD as LCD

# LCD x Raspberry (GPIO) connections
LCD_RS = 18
LCD_EN = 23
LCD_D4 = 12
LCD_D5 = 16
LCD_D6 = 20
LCD_D7 = 21
LCD_BL = 4

# Defines the number of columns and lines
LCD_COLUMNS = 16
LCD_LINES = 2


class Lcd(object):
    """"Class used for LCD manipulation"""
    def __init__(self):
        self.lcd = LCD.Adafruit_CharLCD(LCD_RS, LCD_EN, LCD_D4, LCD_D5, LCD_D6,
                                        LCD_D7, LCD_COLUMNS, LCD_LINES, LCD_BL)

    def show_message(self, message, message2=''):
        """Shows a message in the choosen line
            Parameters: - message: text to be showed
                        - line: 0 or 1
        """
        self.clear_display()
        self.lcd.message(message)
        self.lcd.message("\n" + message2)
        # if line == 0:
        #     self.lcd.message(message)
        # else:
        #     self.lcd.message("\n" + message)

    def clear_display(self):
        """Clear both display lines"""
        self.lcd.clear()

# if __name__ == "__main__":
#     lcd = Lcd()
#     lcd.clear_display()
#     message = 'Arduino e Cia'
#     lcd.show_message(message)
#     message2 = '\nRaspberry  Pi'
#     lcd.show_message(message2)
