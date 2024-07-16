from var.ConfigManager import config

#Database
database_startup_script = f'''
CREATE DATABASE {config.data["database"]["name"]};
USE {config.data["database"]["name"]};
CREATE TABLE Accounts(
Account_ID INT PRIMARY KEY AUTO_INCREMENT,
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
