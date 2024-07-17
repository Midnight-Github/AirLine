import mysql.connector
from var.ConfigManager import config
from reader.Logger import Logger
from errors.Database import DatabaseNotUnique, DatabaseInvalid, DatabaseExecutionError
from inspect import cleandoc

logger = Logger(__name__).logger

class Mysql():
    def __init__(self):
        self.host = config.data["database"]["host"]
        self.user = config.data["database"]["user"]
        self.password = config.data["database"]["password"]
        self.name = config.data["database"]["name"]
        self.force_create = config.data["database"]["force_create"]

        self.startup_script = cleandoc(f'''
        CREATE DATABASE {self.name};
        USE {self.name};
        CREATE TABLE Accounts(
        Name VARCHAR(255) PRIMARY KEY NOT NULL,
        Password VARCHAR(255) NOT NULL,
        Permission INT NOT NULL,
        CHECK (Permission = 0 OR Permission = 1)
        );
        CREATE TABLE Flights(
        Booking_ID INT PRIMARY KEY,
        Name VARCHAR(255) NOT NULL,
        FOREIGN KEY (Name) REFERENCES Accounts(Name)
        );
        ''')
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
            return False

        cursor = db.cursor()
        try:
            cursor.execute("DESC accounts;")
            accounts_info = cursor.fetchall()
            cursor.execute("DESC flights;")
            flights_info = cursor.fetchall()

            is_accounts_valid = accounts_info == [
                ('Name', 'varchar(255)', 'NO', 'PRI', None, ''), 
                ('Password', 'varchar(255)', 'NO', '', None, ''), 
                ('Permission', 'int', 'NO', '', None, '')
            ]

            is_flights_valid = flights_info == [
                ('Booking_ID', 'int', 'NO', 'PRI', None, ''),
                ('Name', 'varchar(255)', 'NO', 'MUL', None, ''), 
            ]

            if not is_accounts_valid or not is_flights_valid:
                raise DatabaseNotUnique("Tables discription are not valid")

        except Exception as e:
            logger.critical("Failed!")
            logger.critical("Database already exists in server!")
            
            if self.force_create:
                logger.warning("Dropping database")
                cursor.execute(f"DROP DATABASE {self.name};")
                return self.create()
            logger.exception(e)
            raise DatabaseNotUnique("required tables not found in database")
        finally:
            cursor.close()

        self.database = db
        logger.info("Connected!")
        return True

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
            cursor.execute(self.startup_script)
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
        return True

    def execute(self, cmd, cmd_args=None, *cursor_args, **cursor_kwargs):
        if self.database == None:
            logger.critical("Error while executing commands to a disconnected database")
            raise DatabaseExecutionError("cannot to execute commands to a disconnected database")
        cursor = self.database.cursor(*cursor_args, **cursor_kwargs)
        try:
            if cmd_args == None:
                cursor.execute(cmd)
            else:
                cursor.execute(cmd, cmd_args)
            self.database.commit()
            return True
        except mysql.connector.Error as e:
            return e
        except Exception as e:
            logger.critical("Error while executing commands")
            logger.exception(e)
            raise DatabaseExecutionError(e)
        finally:
            cursor.close()