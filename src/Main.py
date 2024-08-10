from ui.Manager import Manager
from var.SqlManager import mysql
from var.ConfigManager import appdata
from reader.Logger import Logger
import os
from var.Globals import get_user_position

logger = Logger(__name__).logger

def main():
    os.system('cls')
    logger.info("Welcome to AirLine!")

    connectDatabase()
    if appdata.data["user"]["name"] != "None":
        logUser()

    Manager().mainloop()

def connectDatabase():
    if mysql.connect() is False:
        mysql.create()

def logUser():
    result = mysql.execute(f"SELECT Name from Accounts WHERE Name = '{appdata.data["user"]["name"]}';", buffered=True)
    print(result[1])
    if result[0] is False or not result[1]:
        logger.warning(f"Failed to auto log {get_user_position[appdata.data["user"]["permission"]]}: {appdata.data["user"]["name"]} in")
        appdata.data["user"]["name"] = "None"
        appdata.data["user"]["permission"] = -1
        appdata.push()
        return

    logger.warning(f"Auto logged {get_user_position[appdata.data["user"]["permission"]]}: {appdata.data["user"]["name"]}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception(e)
    finally:
        logger.info("Program terminated!")
    