import atexit
import traitlets
from traitlets.config.configurable import Configurable
from jetbot.drivetrain import MotorDriver


class Motor(Configurable):

    value = traitlets.Float()
    
    # config
    alpha = traitlets.Float(default_value=1.0).tag(config=True)
    beta = traitlets.Float(default_value=0.0).tag(config=True)

    def __init__(self, driver, channel, *args, **kwargs):
        super(Motor, self).__init__(*args, **kwargs)  # initializes traitlets

        self._driver = driver
        self._motor = self._driver.getMotor(channel)
        atexit.register(self._release)
        
    @traitlets.observe('value')
    def _observe_value(self, change):
        self._write_value(change['new'])

    def _write_value(self, value):
        """Sets motor value between [-1, 1]"""
        mapped_value = int(255.0 * (self.alpha * value + self.beta))
        speed = min(max(abs(mapped_value), 0), 255)
        self._motor.set_speed(speed)
        if mapped_value < 0:
            self._motor.run(MotorDriver.FORWARD)
        else:
            self._motor.run(MotorDriver.BACKWARD)

    def _release(self):
        """Stops motor by releasing control"""
        self._motor.run(MotorDriver.RELEASE)
