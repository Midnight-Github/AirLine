from ui.Manager import Manager
from var.SqlManager import mysql
from reader.Logger import Logger
import os

logger = Logger(__name__).logger

def main():
    os.system('cls')
    logger.info("Welcome to AirLine!")

    connectDatabase()
            
    Manager().mainloop()

def connectDatabase():
    if mysql.connect() == False:
        mysql.create()

if __name__ == "__main__":
    main()
    