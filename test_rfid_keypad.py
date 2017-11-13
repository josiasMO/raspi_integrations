# -*- coding: utf-8 -*-

from time import sleep
from threading import Thread, Lock
import signal

from Lcd import Lcd
from Keypad import Keypad
from Buzzer import Buzzer
from Rfid import Rfid


codigo_motorista = ""

keypad = Keypad()
buzzer = Buzzer()
lcd = Lcd()
rfid = Rfid()
lock = Lock()

CARDS = ["[154, 99, 3, 197, 63]", "[151, 25, 214, 53, 109]"]
KEYCHAINS = ["[213, 1, 9, 136, 85]", "[5, 214, 17, 136, 74]"]

control = True

def read_keypad():
    global codigo_motorista, control
    keys = ""
    while control:
        lcd.show_message("Cod Motorista: ", keys)
        key = keypad.read_key()
        if key == "0" or key == "1" or key == "2" or key == "3" or key == "4" or \
                        key == "5" or key == "6" or key == "7" or key == "8" or key == "9":
            keys += key

        elif key == "A":
            lock.acquire()
            try:
                codigo_motorista = keys
                control = False
            finally:
                lock.release()

def read_rfid():
    global codigo_motorista, control
    uid = rfid.read_rfid()
    if uid:
        print(uid)
        lock.acquire()
        try:
            codigo_motorista = CARDS.index(str(uid))
            control = False
        finally:
            lock.release()

def manage_read():
    global codigo_motorista, control
    rfid_reader = Thread(name='read_rfid', target=read_rfid)
    keypad_reader = Thread(name='read_keypad', target=read_keypad)

    rfid_reader.daemon = True
    keypad_reader.daemon = True
    rfid_reader.start()
    keypad_reader.start()

    while control:
        pass

def main():
    global codigo_motorista, control
    read_manager = Thread(name='read_manager', target=manage_read)
    read_manager.start()
    read_manager.join()

    print("Codigo do motorista: ", codigo_motorista)

if __name__ == "__main__":
    main()