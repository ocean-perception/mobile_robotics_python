from datetime import datetime
from pathlib import Path


class Logger:
    def __init__(self):
        self.filename = "./" + self.stamp() + "_log.csv"
        self.filename = Path(self.filename)
        self.file = self.filename.open("w")
        print("[Logger]: Creating logging file at", self.filename)

    @staticmethod
    def stamp():
        stamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        return str(stamp)

    def set_header(self, header):
        self.file.write("stamp," + str(header) + "\n")

    def log(self, *argv):
        arg_str = ""
        for arg in argv:
            arg_str += "," + str(arg)
        self.file.write(self.stamp() + arg_str + "\n")

    def __del__(self):
        # Make sure logging data is written to disk
        # if we decide to stop execution
        print("\n[Logger]: Closing logging file at", self.filename)
