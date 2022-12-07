import time
import weakref

import numpy as np

from mobile_robotics_python import Console
from mobile_robotics_python.messages import SpeedRequestMessage

from . import ActuatorDriverBase
from .maestro_controller import Controller


class PololuMicroMaestro(ActuatorDriverBase):
    def __init__(self, parent=None):
        self.ready = False
        self.name = "pololu_motors"
        if parent is not None:
            self._parent = weakref.ref(parent)

    def init(self, params):
        try:
            self._ctrl = Controller()

            self.left_idx = params["left"]["port"]
            self.right_idx = params["right"]["port"]
            self.tam = np.array(params["tam"]).reshape((2, 2))

            # Expecting a ESC + BLDC in channel 1
            # Set ESC range (3200 - 8000)
            # 5600 is zero speed in quarter microseconds (1400 us)
            # Controllable to 5600 +/- 2400
            # with deadband in 5800-5400
            self._ctrl.setRange(self.left_idx, 3200, 8000)
            self._ctrl.setRange(self.right_idx, 3200, 8000)

            # For ESC to boot, we need to stop at neutral
            self._ctrl.setTarget(self.left_idx, 5600)
            self._ctrl.setTarget(self.right_idx, 5600)
            time.sleep(0.5)
            self._ctrl.setTarget(self.left_idx, 5600)
            self._ctrl.setTarget(self.right_idx, 5600)
            time.sleep(7.0)
            self._ctrl.setTarget(self.left_idx, 5600)
            self._ctrl.setTarget(self.right_idx, 5600)
            time.sleep(0.5)
            self._ctrl.setTarget(self.left_idx, 5600)
            self._ctrl.setTarget(self.right_idx, 5600)
            time.sleep(0.5)

            self.ready = True
        except Exception as e:
            Console.warn("    PololuMotors could not be initialised. Error:", e)
            return

    def move(self, msg: SpeedRequestMessage):
        if not self.ready:
            Console.warn("    PololuMicroMaestro is not ready")
            return SpeedRequestMessage()

        # Use a TAM to transform the speeds to RPMs
        req = np.array([[msg.vx_mps], [msg.wz_radps]])
        rpm = self.tam @ req + 5600
        self._ctrl.setTarget(self.left_idx, int(rpm[0, 0]))
        self._ctrl.setTarget(self.right_idx, int(rpm[1, 0]))
        return msg

    def __del__(self):
        if self.ready:
            Console.info("Stopping the motors...")
            # For ESC to boot, we need to stop at neutral
            self._ctrl.setTarget(self.left_idx, 5600)
            self._ctrl.setTarget(self.right_idx, 5600)
            time.sleep(0.5)
            self._ctrl.setTarget(self.left_idx, 5600)
            self._ctrl.setTarget(self.right_idx, 5600)
            time.sleep(7.0)
            self._ctrl.setTarget(self.left_idx, 5600)
            self._ctrl.setTarget(self.right_idx, 5600)
            time.sleep(0.5)
            self._ctrl.setTarget(self.left_idx, 5600)
            self._ctrl.setTarget(self.right_idx, 5600)
            time.sleep(0.5)
            self._ctrl.close()
