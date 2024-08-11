import customtkinter as ctk
from var.ConfigManager import appdata
from reader.Logger import Logger
from var.SqlManager import mysql
from ui.AddFlight import AddFlight
from var.Globals import get_user_role
from CTkMessagebox import CTkMessagebox as ctkmsgbox
from datetime import datetime
from template.TreeView import TreeView

logger = Logger(__name__).logger

class Flights(TreeView):
    def __init__(self, root):
        super().__init__(root, columns=('ID', 'Airline', 'Place of Departure', 'Destination', 'Class', 'Date', 'Time', 'Price'), heading="Available Flights")

        # example flights
        # ('Indigo','Delhi','Mumbai','Economy', '17:00 - 19:30' ,'5000INR')
        # ('Indigo','Bangalore','Mumbai','Economy', '18:00 - 20:00', '5500INR')
        # ('Emirates','Bangalore','Dubai','First Class', '01:00 - 04:30', '10000INR')

        self.btn_frame = ctk.CTkFrame(self,fg_color='transparent')
        self.btn_frame.grid(row=2,column=0, sticky='se')
        
        self.book_btn = ctk.CTkButton(self.btn_frame, text="Book Flight", command=self.BookFlight)
        self.book_btn.grid(row=0,column=0, padx=5)    
        self.refresh_btn = ctk.CTkButton(self.btn_frame, text="Refresh", command=self.refresh)
        self.refresh_btn.grid(row=0,column=3, padx=5)
        self.back_btn = ctk.CTkButton(self.btn_frame, text="Back", command=lambda : self.root.showFrame("Home"))
        self.back_btn.grid(row=0, column=4, padx=5)

        if appdata.data["user"]["permission"] > 0:
            self.adminFeatures()

        self.refresh()

    def adminFeatures(self):
        self.add_flight_form = None

        self.add_btn = ctk.CTkButton(self.btn_frame, text="Add Flight", command=self.addFlight)
        self.add_btn.grid(row=0, column=1, padx=5)

        self.delete_btn = ctk.CTkButton(self.btn_frame, text="Delete Flight", command=self.deleteFlight)
        self.delete_btn.grid(row=0, column=2, padx=5)

    def formatFlights(self, table):
        for i, row in enumerate(table):
            row = row[:-1] + (str(row[-1]) + 'INR',)
            table[i] = row
        return table

    def isAddFlightFormAlive(self):
        return not (self.add_flight_form is None or not self.add_flight_form.winfo_exists())

    def addFlight(self):
        if not self.isAddFlightFormAlive():
            self.add_flight_form = AddFlight(self.insertRowFlights)
        
        self.add_flight_form.after(100, self.add_flight_form.lift) #pyright: ignore # work around to fix bug: toplevel hiding behind root

    def deleteFlight(self):
        selected = self.getSelectedRow()
        if selected is None:
            ctkmsgbox(title="Flights", message="No flight selected!")
            return
        flight_id = selected[0]
        sql_cmd_del_passengers = f"DELETE FROM Passengers WHERE Flight_ID = {flight_id}"
        sql_cmd_del_flights = f"DELETE FROM Flights WHERE Flight_ID = {flight_id};"
        result_passengers = mysql.execute(sql_cmd_del_passengers)
        result_flights = mysql.execute(sql_cmd_del_flights)

        if result_passengers[0] is False:
            logger.error("Failed to delete data from Passengers!")
            logger.error(result_passengers[1])
            return 
        
        if result_flights[0] is False:
            logger.error("Failed to delete data from Flights!")
            logger.error(result_flights[1])
            return 

        self.refresh()

        logger.info(f"{get_user_role[appdata.data["user"]["permission"]]}: {appdata.data["user"]["name"]} deleted flight with id {flight_id}")
        self.root.reinitFrame("Cart")
        self.root.showFrame("Flights")
        
    def refresh(self):
        logger.info("Refreshing Flights!")
        self.extractFlights()
        self.reloadTable()

    def extractFlights(self):
        date, time = str(datetime.now()).split()

        sql_cmd = f"SELECT * FROM Flights WHERE (Date > DATE('{date}') OR (Date = DATE('{date}') AND Time >= TIME('{time}')));"
        result = mysql.execute(sql_cmd, buffered=True)

        if result[0] is False:
            logger.error("Failed to extract data from Flights!")
            logger.error(result[1])
            return

        self.flights = self.formatFlights(result[1])
        logger.info("Extracted data from flights")

    def reloadTable(self):
        self.deleteAllRows()

        for flight in self.flights:
            self.insertRow(flight)

    def insertRowFlights(self, row):
        sql_cmd = f"INSERT INTO Flights {str(tuple(row.keys())).replace('\'', '')} VALUES {str(tuple(row.values()))};"
        result = mysql.execute(sql_cmd)

        if result[0] is False:
            logger.error("Failed to insert data to Flights!")
            logger.error(result[1])
            return
        
        self.refresh()

        logger.info(f"{get_user_role[appdata.data["user"]["permission"]]}: {appdata.data["user"]["name"]} inserted {row} to Flights")
        if self.isAddFlightFormAlive():
            self.add_flight_form.destroy() # pyright: ignore
            self.add_flight_form.update() # pyright: ignore        
        
    def BookFlight(self):
        flight_id = self.getSelectedRow()
        if flight_id is None:
            ctkmsgbox(title="Flights", message="No flight selected!")
            return

        flight_id = flight_id[0]
        result = mysql.execute(f"INSERT INTO Passengers VALUES('{appdata.data["user"]["name"]}', {flight_id});")
        
        if result[0] is False:
            if "Duplicate entry" in str(result[1]):
                ctkmsgbox(title="Flights", message="You have already booked this flight")
                logger.warning(f"{get_user_role[appdata.data["user"]["permission"]]}: {appdata.data["user"]["name"]} tried to rebook flight with id: {flight_id}")
                return
            logger.error("Failed to insert data to Passengers!")
            logger.error(result[1])
            return
        
        ctkmsgbox(message="Successfully booked flight",icon="check")
        logger.info(f"{get_user_role[appdata.data["user"]["permission"]]}: {appdata.data["user"]["name"]} booked Flight with id: {flight_id}")
        self.root.reinitFrame("Cart")
        self.root.showFrame("Flights")
        return
