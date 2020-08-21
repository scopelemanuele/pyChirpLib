# This script finds any connected chirp
import machine
import chirp

# GREEN == SDA  YELLOW == SCL from https://www.tindie.com/products/miceuz/i2c-soil-moisture-sensor/
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=300000)

for addr in range(0, 127):
    try:
        print("trying {}".format(addr))
        sensor = chirp.Chirp(bus=i2c, address=addr)
        chirp_add = sensor.sensor_address
        print('Sensor Found -- {}'.format(addr))
    except:
        pass
