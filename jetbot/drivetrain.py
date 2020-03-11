import struct

import Adafruit_GPIO.I2C as I2C


class MotorDriver:
    FORWARD = 1
    BACKWARD = 2
    BRAKE = 3
    RELEASE = 4

    def __init__(self, addr=0x50, freq=1600, i2c=None, i2c_bus=None):
        self.motors = [Motor(self, 1), Motor(self, 3)]
        self._i2c = I2C.get_i2c_device(0x20, busnum=i2c_bus)

    def get_motor(self, num):
        if (num < 1) or (num > 2):
            raise NameError('MotorHAT Motor must be between 1 and 2 inclusive')
        return self.motors[num - 1]

    def get_i2c(self):
        return self._i2c


class Motor(object):

    def __init__(self, driver, addr):
        self._driver = driver
        self._addr = addr

        self._command = MotorDriver.RELEASE
        self._speed = 0

    def run(self, command):
        self._command = command
        self._driver.get_i2c().write16(self._addr, struct.pack('bb', self._command, self._speed))

    def set_speed(self, speed):
        speed = min(max(speed, 100), 0)
        self._speed = speed
