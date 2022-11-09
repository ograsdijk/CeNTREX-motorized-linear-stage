import serial


class MotorizedLinearStage:
    """
    Interface between a linear stage driven by a stepper motor controlled by an Arduino Uno
    10_000 steps correspond to 50 mm displacement
    """

    def __init__(self, resource_name: str, timeout: int = 1):
        self.resource_name = resource_name
        self.serial = serial.Serial(resource_name, 9600, timeout=timeout)

    def __exit__(self):
        self.serial.close()

    def __repr__(self):
        return f"MotorizedLinearStage({self.resource_name})"

    @property
    def identity(self) -> str:
        self.serial.write(b"?")
        return self.serial.readline().decode()

    def enable(self):
        self.serial.write(b"e1")

    def disable(self):
        self.serial.write(b"e0")

    def zero(self):
        self.serial.write(b"z")

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
        self.serial.write(f"x{x}".encode())

    @property
    def position(self) -> int:
        """
        Return the current motor position in motor steps. 10_000 steps correspond to 50 mm.

        Returns:
            int: current position in motor steps
        """
        self.serial.write(b"x")
        return int(self.serial.readline())

    def set_dt(self, dt: int):
        if not isinstance(dt, int):
            raise TypeError("dt not integer")
        self.serial.write(f"s{dt}")
