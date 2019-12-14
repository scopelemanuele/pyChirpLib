from machine import Pin, I2C
from time import sleep

# i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=300000)

class Chirp:
    def __init__(self, bus, address=0x20, min_moist=250, max_moist=800):
        self.i2c = bus
        self.address = address
        self.min_moist = min_moist
        self.max_moist = max_moist

    def _bytes_to_int(self, bytes):
        result = 0
        for b in bytes:
            result = result * 256 + int(b)
        return result

    def _int_to_bytes(self, value, length):
        result = []
        for i in range(0, length):
            result.append(value >> (i * 8) & 0xff)
        result.reverse()
        return result

    def get_reg(self, reg, lenght=2):
        val = self.i2c.readfrom_mem(self.address, reg, lenght)
        return self._bytes_to_int(val)
    
    @property
    def sensor_address(self):
        return self.get_reg(0x02,1)

    def reset(self):
        print("Resetting")
        val = self._int_to_bytes(0, 1)
        self.i2c.writeto_mem(self.address, 0x06, bytearray(val))
        sleep(5)
        print("Resetted")

    def set_address(self, new_addr):
        addr = self._int_to_bytes(new_addr, 1)
        self.i2c.writeto_mem(self.address, 0x01, bytearray(addr))
        self.i2c.writeto_mem(self.address, 0x01, bytearray(addr))
        self.reset()
        self.address = new_addr
    
    #Not tested
    """
    def sleep(self):
      
        self.i2c.writeto_mem(self.address, 0x08, bytearray(self._int_to_bytes(0,1)))

    def wake_up(self, wake_time=1):
        try:
            self.get_reg(0x07,1)
        except OSError:
            pass
        finally:
            sleep(wake_time)
    """
    
    @property
    def version(self):
        return self.get_reg(7,1)
    
    @property
    def busy(self):
        busy = self.get_reg(9,1)

        if busy == 1:
            return True
        else:
            return False

    @property
    def moisture(self):
        return self.get_reg(0,2)

    @property
    def temperature(self):
        return self.get_reg(5,2)/10

    def light(self):
        self.i2c.writeto_mem(self.address, 0x03, bytearray(self._int_to_bytes(0,1)))
        sleep(1.5)
        return self.get_reg(4,2)

    @property
    def moist_percent(self):
        moisture = self.moisture
        return round((((moisture - self.min_moist)/(self.max_moist - self.min_moist)) * 100), 1)
        
