from var.Globals import database_manager as dbm

#Database
create_table_accounts = '''
CREATE TABLE Accounts(
Account_ID INT PRIMARY KEY,
Name VARCHAR(255) UNIQUE,
Password VARCHAR(255) NOT NULL,
Permission INT NOT NULL,
CHECK (Permission = 0 OR Permission = 1)
);
'''.replace('\n', '')

create_table_flights = '''
CREATE TABLE Flights(
Booking_ID INT PRIMARY KEY,
Account_ID INT NOT NULL,
FOREIGN KEY (Account_ID) REFERENCES Accounts(Account_ID)
);
'''.replace('\n', '')

database_info = {
    "host": dbm.data["info"]["host"],
    "user": dbm.data["info"]["user"],
    "name": "Airline",
    "password": dbm.data["info"]["password"]
}


