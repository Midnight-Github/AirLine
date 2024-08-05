import mysql.connector
from var.ConfigManager import config
from reader.Logger import Logger
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
        Name VARCHAR(255) PRIMARY KEY,
        Password VARCHAR(255) NOT NULL,
        Permission INT NOT NULL,
        CHECK (Permission = 0 OR Permission = 1)
        );
        CREATE TABLE Flights(
        Flight_ID INT PRIMARY KEY AUTO_INCREMENT,
        Airline VARCHAR(255) NOT NULL,
        Pod VARCHAR(255) NOT NULL,
        Destination VARCHAR(255) NOT NULL,
        Class VARCHAR(255) NOT NULL,
        Date VARCHAR(255) NOT NULL,
        Time VARCHAR(255) NOT NULL,
        Price INT NOT NULL
        );
        CREATE TABLE Passengers(
        Name VARCHAR(255) NOT NULL,
        Flight_ID INT NOT NULL,
        PRIMARY KEY (Name, Flight_ID),
        FOREIGN KEY(Name) REFERENCES Accounts(Name),
        FOREIGN KEY(Flight_ID) REFERENCES Flights(Flight_ID)
        );
        ''')
        self.accounts_table_structure = [
            ('Name', 'varchar(255)', 'NO', 'PRI', None, ''), 
            ('Password', 'varchar(255)', 'NO', '', None, ''), 
            ('Permission', 'int', 'NO', '', None, '')
        ]
        self.flights_table_structure = [
            ('Flight_ID', 'int', 'NO', 'PRI', None, 'auto_increment'), 
            ('Airline', 'varchar(255)', 'NO', '', None, ''), 
            ('Pod', 'varchar(255)', 'NO', '', None, ''), 
            ('Destination', 'varchar(255)', 'NO', '', None, ''), 
            ('Class', 'varchar(255)', 'NO', '', None, ''),
            ('Date', 'varchar(255)', 'NO', '', None, ''),
            ('Time', 'varchar(255)', 'NO', '', None, ''), 
            ('Price', 'int', 'NO', '', None, '')
        ]
        self.passengers_table_structure = [
            ('Name', 'varchar(255)', 'NO', 'PRI', None, ''), 
            ('Flight_ID', 'int', 'NO', 'PRI', None, '')
        ]

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
        except Exception:
            logger.warning("Failed!")
            self.database = None
            return False

        cursor = db.cursor()
        try:
            cursor.execute("DESC accounts;")
            accounts_info = cursor.fetchall()
            cursor.execute("DESC flights;")
            flights_info = cursor.fetchall()
            cursor.execute("DESC passengers;")
            passengers_info = cursor.fetchall()

            is_accounts_valid = accounts_info == self.accounts_table_structure
            is_flights_valid = flights_info == self.flights_table_structure
            is_passengers_valid = passengers_info == self.passengers_table_structure

            if not is_accounts_valid or not is_flights_valid or not is_passengers_valid:
                raise Exception("Database tables are not valid!")

        except Exception as e:
            logger.critical("Failed!")
            logger.critical("Database tables are not valid!")
            
            if self.force_create:
                logger.warning("Dropping database")
                cursor.execute(f"DROP DATABASE {self.name};")
                return self.create()
            raise e
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
            raise e

        try:
            cursor = db.cursor()
            cursor.execute(self.startup_script)
            cursor.close()
            db.close()
        except Exception as e:
            logger.critical("Failed!")
            logger.critical("Error while execution sql startup script")
            raise e

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
            logger.critical("Tried to execute commands to a disconnected database")
            raise Exception("Cannot to execute commands to a disconnected database")
        cursor = self.database.cursor(*cursor_args, **cursor_kwargs)
        try:
            if cmd_args == None:
                cursor.execute(cmd)
            else:
                cursor.execute(cmd, cmd_args)
            self.database.commit()
            return (True, cursor.fetchall())
        except mysql.connector.Error as e:
            return (False, e)
        except Exception as e:
            logger.critical("Error while executing commands")
            raise e
        finally:
            cursor.close()
