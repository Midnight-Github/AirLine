from ui.Manager import Manager
from mysql.connector import connect
from var.Const import database_info, create_table_accounts, create_table_flights

def main():
    connectDatabase(database_info)
    Manager().mainloop()

def createDatabase(db_info):
    print("Creating database")
    try:
        db = connect(
            host=db_info["host"],
            user=db_info["user"],
            password=db_info["password"]
        )
    except Exception:
        print("Error while connecting to database!")
        print("Make sure the host, user and password are correct in file\n'AirLine/src/config/database.toml'")
        exit()

    cursor = db.cursor()
    cursor.execute(f"CREATE DATABASE {database_info["name"]};")
    cursor.execute("USE Airline;")
    cursor.execute(create_table_accounts)
    cursor.execute(create_table_flights)
    db.close()

def connectDatabase(db_info):
    try:
        print("Connecting to database")
        db = connect(
            host=db_info["host"],
            user=db_info["user"],
            password=db_info["password"],
            database=db_info["name"]
        )
        db.close()
        print("Connected")
    except Exception:
        print("Failed")
        createDatabase(db_info)


if __name__ == "__main__":
    main()
    