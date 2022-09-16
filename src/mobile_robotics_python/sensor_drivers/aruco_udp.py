import json
import socket
from threading import Thread

from mobile_robotics_python.messages import RobotStateMessage

from . import SensorDriverBase


class ArUcoUDP(SensorDriverBase):
    def __init__(self, params):
        # -- UDP
        self.client = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP
        )

        # -- Enable port reusage
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # -- Enable broadcasting mode
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # self.client.settimeout(params["timeout"])
        self.client.bind(("", params["port"]))
        self.marker_id = params["marker_id"]
        self.th = Thread(target=self.loop, daemon=True)
        self.th.start()

        # -- data recieved
        self.data = None

    def loop(self):
        while True:
            print("waiting for data...")
            try:
                broadcast_data, _ = self.client.recvfrom(4096)
                result = json.loads(broadcast_data)
                self.data = result.get(str(self.marker_id), None)

            except Exception as e:
                print("Got exception trying to recv %s" % e)

    def read(self, state: RobotStateMessage) -> RobotStateMessage:
        msg = RobotStateMessage()
        if self.data is None:
            return None
        msg.stamp_s = self.data[0]
        msg.x_m = self.data[2]
        msg.y_m = self.data[3]
        msg.z_m = self.data[4]
        msg.roll_rad = self.data[5]
        msg.pitch_rad = self.data[6]
        msg.yaw_rad = self.data[7]
        return msg

    def __del__(self):
        self.client.close()
