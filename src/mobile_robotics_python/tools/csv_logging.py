from datetime import datetime
from pathlib import Path


class Logger:
    def __init__(self, name: str, logging_folder: str):
        mission_folder = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = self.stamp() + "_" + name + "_log.csv"
        logging_folder_path = Path(logging_folder) / mission_folder
        if not logging_folder_path.exists():
            logging_folder_path.mkdir(parents=True, exist_ok=True)
        self.filename = logging_folder_path / filename
        self.file = self.filename.open("w")
        print("[Logger]: Creating logging file at", self.filename)

    @staticmethod
    def stamp():
        stamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
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
