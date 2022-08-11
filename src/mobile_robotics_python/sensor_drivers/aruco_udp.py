import socket
from threading import Thread

from mobile_robotics_python import Rate
from mobile_robotics_python.messages import RobotStateMessage
import json

class ArUcoUDP:
    def __init__(self, params):
        # -- UDP
        self.client = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP
        )

        # -- Enable port reusage
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # -- Enable broadcasting mode
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.client.settimeout(params["timeout"])
        self.client.bind(("", params["port"]))
        self.aruco_id = params['aruco_id']
        self.th = Thread(target=self.loop, daemon=True)
        self.th.start()

        # -- data recieved
        self.data = [None]*8

    def loop(self):
        r = Rate(10)
        while True:
            try :
                broadcast_data, _ = self.client.recvfrom(1024)
                result = json.loads(broadcast_data)
                self.data = result.get(str(self.aruco_id), None)

            except Exception as e:
                print("Got exception trying to recv %s" % e)
                raise StopIteration
            r.sleep()

    def read(self) -> RobotStateMessage:
        # TODO convert self.data to RobotStateMessage
        msg = RobotStateMessage()
        if self.data is None:
            return msg
        msg.stamp_s = self.data[0]
        msg.x_m = self.data[2]
        msg.y_m = self.data(3)
        msg.z_m = self.data(4)
        msg.roll_rad = self.data(5)
        msg.pitch_rad = self.data(6)
        msg.yaw_rad = self.data(7)

    def __del__(self):
        self.client.close()
