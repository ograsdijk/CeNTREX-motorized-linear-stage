import pyvisa
import time

class MotorizedLinearStage:
    """
    Interface between a linear stage driven by a stepper motor controlled by an Arduino Uno
    10_000 steps correspond to 50 mm displacement
    """

    def __init__(self, resource_name: str, timeout: int = 10_000):
        self.resource_name = resource_name
        self.rm = pyvisa.ResourceManager()
        self.device = self.rm.open_resource(resource_name, baud_rate=9600, timeout=timeout, access_mode=4)

    def __exit__(self):
        self.device.close()

    def __repr__(self):
        return f"MotorizedLinearStage({self.resource_name})"

    @property
    def identity(self) -> str:
        self.device.write("?")

        identity = ""
        while True:
            try:
                ret = self.device.read()
                identity += ret
            except pyvisa.VisaIOError:
                break
        return identity

    def enable(self):
        self.device.write("e1")

    def disable(self):
        self.device.write("e0")

    def zero(self):
        self.device.write("z")

    def move(self, x: int):
        """
        Move the linear stage to position x in motor steps. 10_000 steps correspond to 50 mm

        Args:
            x (int): position to move to

        Raises:
            TypeError: error if x is not integer
        """
        if not isinstance(x, int):
            raise TypeError("x not integer")
        self.enable()
        self.device.write(f"m{x}")

    @property
    def position(self) -> int:
        """
        Return the current motor position in motor steps. 10_000 steps correspond to 50 mm.

        Returns:
            int: current position in motor steps
        """
        return int(self.device.query("x"))

    def set_dt(self, dt: int):
        if not isinstance(dt, int):
            raise TypeError("dt not integer")
        self.device.write(f"s{dt}")
