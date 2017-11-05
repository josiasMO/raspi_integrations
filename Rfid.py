#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
from time import sleep

#continue_reading = True


class Rfid(object):
    ''''''
    def __init__(self):
        self.reader = MFRC522.MFRC522()

    def read_rfid_uid(self):
        status, TagType = self.reader.MFRC522_Request(self.reader.PICC_REQIDL)

        # # If a card is found
        # if status == self.reader.MI_OK:
        #     print "Card detected"

        # Get the UID of the card
        status, uid = self.reader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == self.reader.MI_OK:
            return uid

#
# # Capture SIGINT for cleanup when the script is aborted
# def end_read(signal,frame):
#     global continue_reading
#     print "Ctrl+C captured, ending read."
#     continue_reading = False
#     GPIO.cleanup()
#     exit(1)
#
# # Hook the SIGINT
# signal.signal(signal.SIGINT, end_read)
#
#
# if __name__ == '__main__':
#     rfid_reader =  Rfid()
#
#     while True:
#         uid = rfid_reader.read_rfid_uid()
#         if uid:
#             print(uid)