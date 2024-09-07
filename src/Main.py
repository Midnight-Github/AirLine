from ui.Manager import Manager
from var.SqlManager import mysql
from var.ConfigManager import appdata, config
from reader.Logger import Logger
import os
from var.Globals import get_user_role
from time import sleep
from faker import Faker
import random

# CONSTANTS
# random flight generator
DEFAULT_AVAILABLE_FLIGHTS_LIMIT = config.data["random_flight_generator"]["default_available_flights_limit"]
DEFAULT_EXPIRED_FLIGHTS_LIMIT = config.data["random_flight_generator"]["default_expired_flights_limit"]
YEAR_BIAS = config.data["random_flight_generator"]["year_bias"]
FLIGHT_PRICE_RANGE = (config.data["random_flight_generator"]["flight_price_lower_limit"], config.data["random_flight_generator"]["flight_price_upper_limit"])

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
        logger.info("Inserting default flights...")
        sleep(1) # ig mysql needs some rest.
        insertDefaultFlights(DEFAULT_AVAILABLE_FLIGHTS_LIMIT, YEAR_BIAS)
        insertDefaultFlights(DEFAULT_EXPIRED_FLIGHTS_LIMIT, -YEAR_BIAS)

def generateFlight(year_bias):
    fake = Faker()
    flight_names = ('Air India', 'IndiGo', 'SpiceJet', 'GoAir', 'Vistara', 'AirAsia India', 'Alliance Air', 'Akasa Air', 'Star Air', 'Air India Express')
    states = ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam, Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']
    flight_classes = ('Economy Class', 'Premium Economy Class', 'Business Class', 'First Class')

    if year_bias > 0:
        rand_date, rand_time = fake.future_datetime(end_date=f'+{year_bias}y').strftime('%Y-%m-%d %H:%M:%S').split()
    elif year_bias < 0:
        rand_date, rand_time = fake.past_datetime(start_date=f'-{abs(year_bias)}y').strftime('%Y-%m-%d %H:%M:%S').split()
    elif year_bias == 0:
        rand_date, rand_time = fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S').split()
    else:
        raise ValueError("Invalid year_bias!")

    rand_state = random.choice(states)
    states.remove(rand_state)
    flight_details = {
        "name": random.choice(flight_names),
        "pod": rand_state,
        "dest": random.choice(states),
        "class": random.choice(flight_classes),
        "date": rand_date,
        "time": rand_time,
        "price": random.randrange(*FLIGHT_PRICE_RANGE)
    }
    return flight_details

def insertDefaultFlights(limit, year_bias):
    for _ in range(limit):
        flight_details = generateFlight(year_bias)
        result = mysql.execute(f'''INSERT INTO Flights VALUES(
            NULL, 
            '{flight_details["name"]}', 
            '{flight_details["pod"]}', 
            '{flight_details["dest"]}', 
            '{flight_details["class"]}', 
            '{flight_details["date"]}', 
            '{flight_details["time"]}', 
            {flight_details["price"]} 
            );
        ''')
        if result[0] is False:
            logger.error(f"Failed to insert flight: {flight_details}!")
            logger.error(result[1])
            continue
        logger.info(f"Inserted flight: {flight_details}")

def logUser():
    result = mysql.execute(f"SELECT Name from Accounts WHERE Name = '{appdata.data["user"]["name"]}';", buffered=True)
    if result[0] is False or not result[1]:
        logger.warning(f"Failed to auto log {get_user_role[appdata.data["user"]["permission"]]}: {appdata.data["user"]["name"]} in")
        appdata.data["user"]["name"] = "None"
        appdata.data["user"]["permission"] = -1
        appdata.push()
        return

    logger.warning(f"Auto logged {get_user_role[appdata.data["user"]["permission"]]}: {appdata.data["user"]["name"]}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception(e)
    finally:
        mysql.close()
        logger.info("Program terminated!")
    