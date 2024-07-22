import logging
import os
from datetime import datetime

logs_path = os.path.dirname(__file__) + "\\..\\logs"
logging.basicConfig(level=logging.INFO, format="[%(asctime)s][%(name)s][%(levelname)s]: %(message)s")

def saveLog():
    limit = 3
    limit += 1
    with open(logs_path + "\\latest.log", 'r') as f:
        data = f.read()
    
    with open(logs_path + "\\latest.log", 'w') as f:
        f.write('')

    new_file_name = f"{datetime.now().strftime("%y-%m-%d--%H-%M-%S")}.log"
    with open(logs_path + '\\' + new_file_name, 'w') as f:
        f.write(data)

    logs = os.listdir(logs_path)
    if len(logs) > limit:
        os.remove(logs_path + '\\' + sorted(logs)[0])

saveLog()

class Logger():
    def __init__(self, name):
        self.path = logs_path + "\\latest.log"
        self.logger = logging.getLogger(name)
        handler = logging.FileHandler(self.path, 'a')
        formatter = logging.Formatter("[%(asctime)s][%(name)s][%(levelname)s]: %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
