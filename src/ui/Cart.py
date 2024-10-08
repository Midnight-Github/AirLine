import customtkinter as ctk
from var.ConfigManager import server_config
from reader.Logger import Logger
from var.SqlManager import mysql
from var.Globals import get_user_role
from CTkMessagebox import CTkMessagebox as ctkmsgbox
from datetime import datetime
from widget.TreeView import TreeView

logger = Logger(__name__).logger

class Cart(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root)

        self.root = root

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.heading_label = ctk.CTkLabel(self, text="Booked Flights", font=ctk.CTkFont(size=30, weight="bold"))
        self.heading_label.grid(row=0, column=0, columnspan=2, pady=5)

        self.tree_view = TreeView(self, columns=('ID', 'Airline', 'Place of Departure', 'Destination', 'Class', 'Date', 'Time', 'Price'))
        self.tree_view.grid(row=1, column=1, sticky="nesw")

        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.grid(row=1, column=0, sticky='n', padx=10)

        self.refresh_btn = ctk.CTkButton(self.btn_frame, text="Refresh", command=self.refresh)
        self.refresh_btn.grid(row=0, column=0, padx=10, pady=(10, 20))
        self.cancel_flight_btn = ctk.CTkButton(self.btn_frame, text="Cancel Flight", command=self.cancelFlight)
        self.cancel_flight_btn.grid(row=1, column=0, padx=10, pady=(0, 20))
        self.back_btn = ctk.CTkButton(self.btn_frame, text="Back", command=lambda : self.root.showFrame("Home"))
        self.back_btn.grid(row=2, column=0, padx=10, pady=(0, 10))

        self.refresh()
    
    def refresh(self):
        logger.info("Refreshing Cart!")
        self.tree_view.reloadTable(self.getRowsBookedFlights())

    def cancelFlight(self):
        selected = self.tree_view.getSelectedRow()
        if selected is None:
            ctkmsgbox(title="Cancel flight", message="No flight selected!")
            return

        msg = ctkmsgbox(title="Cancel flight", message="Are you sure you want to cancel this flight!", icon="question", option_1="Yes", option_2="No")
        if msg.get() != "Yes":
            return

        self.deleteRowPassengers(selected[0]) # passing flight id
            
        self.tree_view.deleteRow()
        self.refresh()

        ctkmsgbox(title="Cancel flight", message="Successfully canceled this flight", icon="check")

    # database functions:
    def getRowsBookedFlights(self):
        date, time = str(datetime.now()).split()

        sql_cmd = f"SELECT Flight_ID, Airline, Place_of_departure, Destination, Class, Date, Time, Price FROM Flights NATURAL JOIN Passengers WHERE Name = '{server_config.data["user"]["name"]}' AND (Date > DATE('{date}') OR (Date = DATE('{date}') AND Time >= TIME('{time}')));"
        result = mysql.execute(sql_cmd, buffered=True)

        if result[0] is False:
            logger.error("Failed to extract data from Passengers")
            logger.error(result[1])
            return None
        
        logger.info("Extracted data from passengers")
        return result[1]

    def deleteRowPassengers(self, flight_id):
        sql_cmd_del_passengers = f"DELETE FROM Passengers WHERE Flight_ID = {flight_id};"
        result = mysql.execute(sql_cmd_del_passengers)

        if result[0] is False:
            logger.error("Failed to delete data from Passengers!")
            logger.error(result[1])
            return

        logger.info(f"{get_user_role[server_config.data["user"]["permission"]]}: {server_config.data["user"]["name"]} canceled flight with id {flight_id}")