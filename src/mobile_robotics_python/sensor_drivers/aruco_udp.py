from mobile_robotics_python.messages import RobotStateMessage


import socket


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
        listeningAddress = ("", params["port"])
        self.client.bind(listeningAddress)
        self.loop()

    def loop(self):
        while True:
            self.data, _ = self.client.recvfrom(1024)

    def read(self) -> RobotStateMessage:
        # TODO convert self.data to RobotStateMessage
        pass
