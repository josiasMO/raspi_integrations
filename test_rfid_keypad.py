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
rfid = Rfid()
lock = Lock()

CARDS = ["[154, 99, 3, 197, 63]", "[151, 25, 214, 53, 109]"]
KEYCHAINS = ["[213, 1, 9, 136, 85]", "[5, 214, 17, 136, 74]"]


def read_keypad():
    global codigo_motorista
    key = keypad.read_key()

    if key == "0" or key == "1" or key == "2" or key == "3" or key == "4" or \
                    key == "5" or key == "6" or key == "7" or key == "8" or key == "9":

        lock.acquire()
        try:
            codigo_motorista += key
        finally:
            lock.release()



def read_rfid():
    global codigo_motorista
    while True:
        uid = rfid.read_rfid_uid()
        if uid:
            # print(uid)
            lock.acquire()
            try:
                codigo_motorista = CARDS.index(str(uid))
            finally:
                lock.release()
                


def print_value():
    global codigo_motorista
    while True:
        lock.acquire()
        try:
            print("Codigo do motorista", codigo_motorista)
        finally:
            lock.release()
        sleep(1)


def main():
    rfid_reader = Thread(name='read_rfid', target=read_rfid)
    #keypad_reader = Thread(name='read_keypad', target=read_keypad)
    print_codigo = Thread(name='print_value', target=print_value)

    rfid_reader.start()
    #keypad_reader.start()
    print_codigo.start()


    rfid_reader.join()
   # keypad_reader.join()
    print_codigo.join()



if __name__ == "__main__":
    main()