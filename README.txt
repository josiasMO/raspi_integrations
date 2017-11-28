-----Instalation-----
sudo apt-get update
sudo apt-get install build-essential python-dev python-smbus python-pip git
sudo pip install RPi.GPIO
sudo apt-get install python3-rpi.gpio
sudo pip3 install pyserial

cd ~
git clone https://github.com/adafruit/Adafruit_Python_CharLCD.git
cd Adafruit_Python_CharLCD
sudo python3 setup.py install

cd ~/sysjourney/crx1_tracker
chmod +x ./ppp-creator.sh
sudo ./ppp-creator.sh APN ttySERIAL
