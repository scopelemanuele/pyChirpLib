# This is your main script.
import machine
import chirp
from time import sleep

i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=300000)
sensor = chirp.Chirp(bus=i2c, address=0x20)
print("Sensor Ready")
while True:
    print("moisture: ", sensor.moisture)
    print("temp: ", sensor.temperature)
    sleep(5)
