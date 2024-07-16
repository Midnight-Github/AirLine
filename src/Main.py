from ui.Manager import Manager
from var.SqlManager import mysql
from utils.Logger import Logger
import os

logger = Logger(__name__).logger

def main():
    os.system('cls')
    logger.info("Welcome to AirLine!")

    connectDatabase()
            
    Manager().mainloop()

def connectDatabase():
    mysql.connect()
    if mysql.database == None:
        mysql.create()

if __name__ == "__main__":
    main()
    