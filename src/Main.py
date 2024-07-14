from ui.Manager import Manager
from mysql.connector import connect
from var.Const import database, database_startup_script
from utils.Logger import Logger

logger = Logger(__name__).logger

def main():
    logger.info("Welcome to AirLine!")

    connectDatabase(database)

    Manager().mainloop()

def createDatabase(db_info):
    try:
        db = connect(
            host=db_info["host"],
            user=db_info["user"],
            password=db_info["password"]
        )
        logger.info(f"Created database {database["name"]}")
    except Exception:
        logger.critical("Failed to create database! Make sure the host, user and password are correct")
        exit()

    cursor = db.cursor()
    cursor.execute(f"CREATE DATABASE {database["name"]};")
    cursor.execute("USE Airline;")
    cursor.execute(database_startup_script)
    db.close()

def connectDatabase(db_info):
    try:
        db = connect(
            host=db_info["host"],
            user=db_info["user"],
            password=db_info["password"],
            database=db_info["name"]
        )
        db.close()
        logger.info("Connected to database")

    except Exception:
        logger.warning("Failed to connect to database")
        createDatabase(db_info)


if __name__ == "__main__":
    main()
    