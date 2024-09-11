from ui.Manager import Manager
from var.SqlManager import mysql
from var.ConfigManager import server_config, config
from reader.Logger import Logger
import os
from var.Globals import get_user_role
from time import sleep
from faker import Faker
import random

logger = Logger(__name__).logger
fake = Faker()

def main():
    os.system('cls')
    logger.info("Welcome to AirLine!")

    connectDatabase()
    if server_config.data["user"]["name"] != "None":
        logUser()

    Manager().mainloop()

def connectDatabase():
    if mysql.connect() is False:
        mysql.create()
        logger.info("Inserting default flights...")
        sleep(1) # ig mysql needs some rest.

        available_flights_limit = config.data["random_flight_generator"]["available_flights_limit"]
        expired_flights_limit = config.data["random_flight_generator"]["expired_flights_limit"]
        year_bias = config.data["random_flight_generator"]["year_bias"]

        flight_names = tuple(config.data["flight_info"]["flight_names"])
        states = tuple(config.data["flight_info"]["states"])
        flight_classes = tuple(config.data["flight_info"]["flight_classes"])

        insertDefaultFlights(available_flights_limit, year_bias, flight_names, flight_classes, states)
        insertDefaultFlights(expired_flights_limit, -year_bias, flight_names, flight_classes, states)

def generateFlight(year_bias, flight_names, flight_classes, states):
    if year_bias > 0:
        rand_date, rand_time = fake.future_datetime(end_date=f'+{year_bias}y').strftime('%Y-%m-%d %H:%M:%S').split()
    elif year_bias < 0:
        rand_date, rand_time = fake.past_datetime(start_date=f'-{abs(year_bias)}y').strftime('%Y-%m-%d %H:%M:%S').split()
    elif year_bias == 0:
        rand_date, rand_time = fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S').split()
    else:
        raise ValueError("Invalid year_bias!")

    rand_int1 = random.randint(0, len(states) - 1)
    rand_int2 = random.randint(0, len(states) - 1)
    while rand_int1 == rand_int2:
        rand_int2 = random.randint(0, len(states) - 1)

    flight_details = {
        "name": random.choice(flight_names),
        "pod": states[rand_int1],
        "dest": states[rand_int2],
        "class": random.choice(flight_classes),
        "date": rand_date,
        "time": rand_time,
        "price": random.randrange(config.data["random_flight_generator"]["flight_price_lower_limit"], config.data["random_flight_generator"]["flight_price_upper_limit"])
    }
    return flight_details

def insertDefaultFlights(limit, year_bias, flight_names, flight_classes, states):
    for _ in range(limit):
        flight_details = generateFlight(year_bias, flight_names, flight_classes, states)
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
    result = mysql.execute(f"SELECT Name from Accounts WHERE Name = '{server_config.data["user"]["name"]}';", buffered=True)
    if result[0] is False or not result[1]:
        logger.warning(f"Failed to auto log {get_user_role[server_config.data["user"]["permission"]]}: {server_config.data["user"]["name"]} in")
        server_config.data["user"]["name"] = "None"
        server_config.data["user"]["permission"] = -1
        server_config.data["user"]["show_flights_by"] = "available"
        server_config.push()
        return

    logger.warning(f"Auto logged {get_user_role[server_config.data["user"]["permission"]]}: {server_config.data["user"]["name"]}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception(e)
    finally:
        mysql.close()
        logger.info("Program terminated!")
    