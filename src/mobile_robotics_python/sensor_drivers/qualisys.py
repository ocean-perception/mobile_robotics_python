import asyncio
import importlib
import math
import weakref
from datetime import datetime
from threading import Thread

from mobile_robotics_python.messages import RobotStateMessage
from mobile_robotics_python.tools import Console

from . import SensorDriverBase

qtm_spec = importlib.util.find_spec("qtm")
if qtm_spec is None:
    print("qtm module not found")
    print("Please install the qtm module")
    print("pip install qtm")
else:
    import qtm


def is_valid(x):
    return (not math.isnan(x)) and type(x) == float


class Qualisys(SensorDriverBase):
    def __init__(self, params, parent=None):
        if parent is not None:
            self._parent = weakref.ref(parent)
        self.marker_id = params.get("marker_id", 1)
        self.qualisys_ip = params.get("qualisys_ip", "192.168.0.71")

        Console.info("Starting Qualisys driver")
        Console.info("  * Qualisys IP: " + str(self.qualisys_ip))
        Console.info("  * Marker ID: " + str(self.marker_id))

        # total elapsed simulation time
        self.elapsed_time = 0.0
        self.thread = None
        self.is_connected = False
        self.last_msg = None

        if qtm_spec is not None:
            self.client = asyncio.new_event_loop()
            self.thread = Thread(target=self.start_background_loop)
            self.thread.daemon = True  # Daemonize thread
            self.thread.start()

    def start_background_loop(self):
        asyncio.set_event_loop(self.client)
        asyncio.ensure_future(self.loop())
        self.client.run_forever()

    async def loop(self):
        """Main function"""
        Console.info(
            "Trying to connect to Qualisys server in: " + str(self.qualisys_ip)
        )
        connection = await qtm.connect(self.qualisys_ip)

        if connection is None:
            # TODO: Here we can try to connect to the fake server,
            # that must meet the same qtm data structure
            Console.warn("No active server found in:" + str(self.qualisys_ip))
            self.is_connected = False
            return
        try:
            self.is_connected = True
            _ = await connection.get_state()
            await connection.stream_frames(
                frames="frequency:5",
                components=["6dEuler"],
                on_packet=self.on_packet,
            )
        except asyncio.TimeoutError:
            self.is_connected = False
            return

    def on_packet(self, packet):
        """Callback function that is run when stream-data is triggered by QTM"""
        _, bodies = packet.get_6d_euler()
        stamp = datetime.utcnow()
        stamp = datetime.timestamp(stamp)
        if len(bodies) > self.marker_id:
            self.last_msg = (stamp, bodies[self.body_number])

    def read(self, state: RobotStateMessage) -> RobotStateMessage:
        msg = RobotStateMessage()
        if self.last_msg is None:
            return None

        stamp, body = self.last_msg
        x_mm = body[0][0]  # These are floats
        y_mm = body[0][1]
        z_mm = body[0][2]
        roll_deg = body[1][0]
        pitch_deg = body[1][1]
        yaw_deg = body[1][2]

        # Check if qualisys has valid data
        if is_valid(x_mm) and is_valid(y_mm) and is_valid(z_mm):
            msg.stamp_s = stamp
            msg.x = x_mm / 1000.0
            msg.y = y_mm / 1000.0
            msg.z = z_mm / 1000.0
            msg.roll = roll_deg * math.pi / 180.0
            msg.pitch = pitch_deg * math.pi / 180.0
            msg.yaw = yaw_deg * math.pi / 180.0
            self.last_msg = None
            return msg
        return None

    def __del__(self):
        if self.client.is_running:
            self.client.stop()
        if not self.client.is_closed:
            self.client.close()
