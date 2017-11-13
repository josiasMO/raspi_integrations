from mpu6050 import mpu6050
from time import sleep

sensor = mpu6050(0x68)


accel_x = 0
accel_y = 0
accel_z = 0
try:
    while True:
        accel_data = sensor.get_accel_data()

        x = accel_data['x']
        y = accel_data['y']
        z = accel_data['z']

        print(round(accel_x - x, 2) + round(accel_y - y, 2) + round(accel_z - z, 2))

        accel_x = x
        accel_y = y
        accel_z = z

        sleep(0.1)
except KeyboardInterrupt:
    exit(0)