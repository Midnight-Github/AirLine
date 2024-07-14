from var.Globals import config

#Database
database_startup_script = '''
CREATE TABLE Accounts(
Account_ID INT PRIMARY KEY,
Name VARCHAR(255) UNIQUE,
Password VARCHAR(255) NOT NULL,
Permission INT NOT NULL,
CHECK (Permission = 0 OR Permission = 1)
);
CREATE TABLE Flights(
Booking_ID INT PRIMARY KEY,
Account_ID INT NOT NULL,
FOREIGN KEY (Account_ID) REFERENCES Accounts(Account_ID)
);
'''.replace('\n', '')

database_info = {
    "host": config.data["database"]["host"],
    "user": config.data["database"]["user"],
    "name": "Airline",
    "password": config.data["database"]["password"]
}


