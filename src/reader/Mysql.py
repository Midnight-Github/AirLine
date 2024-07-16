import mysql.connector
from var.Const import database_startup_script
from var.ConfigManager import config
from utils.Logger import Logger
from errors.Database import DatabaseNotUnique, DatabaseInvalid, DatabaseExecutionError

logger = Logger(__name__).logger

class Mysql():
    def __init__(self):
        self.host = config.data["database"]["host"]
        self.user = config.data["database"]["user"]
        self.password = config.data["database"]["password"]
        self.name = config.data["database"]["name"]
        self.force_create = config.data["database"]["force_create"]
        self.database = None

    def connect(self):
        logger.info("Connecting to database")
        try:
            db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.name
            )
        except Exception as e:
            logger.warning("Failed!")
            self.database = None
            return

        cursor = db.cursor()
        try:
            cursor.execute("DESC accounts;")
            accounts_info = cursor.fetchall()
            cursor.execute("DESC flights;")
            flights_info = cursor.fetchall()

            is_accounts_valid = accounts_info == [
                ('Account_ID', 'int', 'NO', 'PRI', None, 'auto_increment'), 
                ('Name', 'varchar(255)', 'YES', 'UNI', None, ''), 
                ('Password', 'varchar(255)', 'NO', '', None, ''), 
                ('Permission', 'int', 'NO', '', None, '')
            ]

            is_flights_valid = flights_info == [
                ('Booking_ID', 'int', 'NO', 'PRI', None, ''),
                ('Account_ID', 'int', 'NO', 'MUL', None, '')
            ]

            if not is_accounts_valid or not is_flights_valid:
                raise DatabaseNotUnique("Tables discription are not valid")

        except Exception as e:
            logger.critical("Failed!")
            logger.critical("Database already exists in server!")
            
            if self.force_create:
                logger.warning("Dropping database")
                cursor.execute(f"DROP DATABASE {self.name};")
                self.create()
                return
            logger.exception(e)
            raise DatabaseNotUnique("required tables not found in database")
        finally:
            cursor.close()

        self.database = db
        logger.info("Connected!")

    def create(self):
        logger.info("Creating Database")
        try:
            db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
            )
        except Exception as e:
            logger.critical("Failed!")
            logger.critical("Make sure host, user and password are correct!")
            logger.exception(e)
            raise DatabaseInvalid(e)

        try:
            cursor = db.cursor()
            cursor.execute(database_startup_script)
            cursor.close()
            db.close()
        except Exception as e:
            logger.critical("Failed!")
            logger.critical("Error while execution sql startup script")
            logger.exception(e)
            raise DatabaseExecutionError(e)

        db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.name
        )
        self.database = db

    def execute(self, cmd, args=None):
        if self.database == None:
            logger.critical("Error while executing commands to a disconnected database")
            raise DatabaseExecutionError("cannot to execute commands to a disconnected database")
        cursor = self.database.cursor()
        try:
            if args == None:
                cursor.execute(cmd)
            else:
                cursor.execute(cmd, args)
            cursor.close()
            return True
        except Exception as e:
            logger.critical("Error while executing commands")
            logger.exception(e)
            raise DatabaseExecutionError(e)
        finally:
            cursor.close()