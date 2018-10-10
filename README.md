# Raspberry Pi Integrations

This project shows integrations between Raspberry Pi and the following devices:

* RFID MFRC522
* LCD 16x2
* Membrane Keypad
* GPS Tracker CRX1
* Buzzer

It has also a real example, using multiple threads in Python and connecting all the peripherals above.

## Requirements

#### Instalation

1) Raspbian and Python:
    
        sudo apt-get update
        sudo apt-get install build-essential python-dev python-smbus python-pip git python3-dev
        sudo pip install RPi.GPIO
        sudo apt-get install python3-rpi.gpio
        sudo pip3 install pyserial
 
2) LCD:

        git clone https://github.com/adafruit/Adafruit_Python_CharLCD.git
        cd Adafruit_Python_CharLCD
        sudo python3 setup.py install

3) CRX1 Tracker:
    
        cd ~/raspi_integrations/crx1_tracker
        chmod +x ./ppp-creator.sh
        sudo ./ppp-creator.sh APN ttySERIAL

4) RFID:

        sudo raspi-config
          5 Interfacing Options
            P4 SPI
              Enable: Yes
                
        cd ~/raspi_integrations/pi-rcr22/
        sudo python3 setup.py install