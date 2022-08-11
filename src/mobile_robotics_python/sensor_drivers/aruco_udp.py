import socket
from threading import Thread

from mobile_robotics_python import Rate
from mobile_robotics_python.messages import RobotStateMessage


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
        self.th = Thread(target=self.loop, daemon=True)
        self.th.start()

    def loop(self):
        r = Rate(10)
        while True:
            try:
                self.data, _ = self.client.recvfrom(1024)
            except Exception as e:
                print("Got exception trying to recv %s" % e)
                raise StopIteration
            r.sleep()

    def read(self) -> RobotStateMessage:
        # TODO convert self.data to RobotStateMessage
        pass

    def __del__(self):
        self.client.close()
