from ui.Manager import Manager
from var.SqlManager import mysql
from var.ConfigManager import appdata
from reader.Logger import Logger
import os

logger = Logger(__name__).logger

def main():
    os.system('cls')
    logger.info("Welcome to AirLine!")

    connectDatabase()

    Manager().mainloop()

def connectDatabase():
    if mysql.connect() is False:
        appdata.data["user"]["name"] = "None"
        appdata.data["user"]["permission"] = -1
        appdata.push()
        mysql.create()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception(e)
    finally:
        logger.info("Program terminated!")
    