import signal
import time

from pirc522 import RFID


class Rfid(object):
    def __init__(self):
        self.rdr = RFID()
        util = self.rdr.util()
        util.debug = False

    def read_rfid(self):
        not_read = True
        while not_read:
            #Request tag
            (error, data) = self.rdr.request()
            if not error:
                (error, uid) = self.rdr.anticoll()
                if not error:
                    not_read = True
                    return uid


if __name__ == '__main__':
    rfid = Rfid()

    while True:
        print(rfid.read_rfid())