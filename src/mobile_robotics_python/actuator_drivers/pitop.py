from pitop.robotics.drive_controller import DriveController

from mobile_robotics_python import Console
from mobile_robotics_python.messages import SpeedRequestMessage


class PiTopMotors:
    def __init__(self, params):
        self.ready = False
        try:
            self._ctrl = DriveController(
                params["left"]["port"], params["right"]["port"]
            )
            self._ctrl.wheel_separation = params["wheel_separation"]
            self._ctrl.stop()
            self.ready = True
        except Exception as e:
            Console.warn("    PiTopMotors could not be initialised. Error:", e)
            return

    def move(self, msg: SpeedRequestMessage):
        if not self.ready:
            Console.warn("    PiTopMotors are not ready")
            return SpeedRequestMessage()
        self._ctrl.robot_move(msg.vx_mps, msg.wz_radps)

    def __del__(self):
        if self.ready:
            self._ctrl.stop()
