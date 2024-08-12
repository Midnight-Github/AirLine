import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from var.ConfigManager import appdata
from reader.Logger import Logger
from var.SqlManager import mysql
from var.Globals import get_user_role
from CTkMessagebox import CTkMessagebox as ctkmsgbox
from datetime import datetime
from template.TreeView import TreeView

logger = Logger(__name__).logger

class Cart(TreeView):
    def __init__(self, root):
        super().__init__(root, columns=('ID', 'Airline', 'Place of Departure', 'Destination', 'Class', 'Date', 'Time', 'Price'), heading="Booked Flights")

        self.btn_frame = ctk.CTkFrame(self,fg_color='transparent')
        self.btn_frame.grid(row=2,column=0,sticky='se')
        self.cancel_flight_btn = ctk.CTkButton(self.btn_frame, text="Cancel Flight", command=self.cancelFlight)
        self.cancel_flight_btn.grid(row=0,column=0, padx=5)
        self.refresh_btn = ctk.CTkButton(self.btn_frame, text="Refresh", command=self.refresh)
        self.refresh_btn.grid(row=0,column=1, padx=5)
        self.back_btn = ctk.CTkButton(self.btn_frame, text="Back", command=lambda : self.root.showFrame("Home"))
        self.back_btn.grid(row=0, column=2, padx=5)

        self.refresh()
    
    def refresh(self):
        logger.info("Refreshing Cart!")
        self.reloadTable(self.getRowsBookedFlights())

    def cancelFlight(self):
        selected = self.getSelectedRow()
        if selected is None:
            ctkmsgbox(title="Cancel flight", message="No flight selected!")
            return

        msg = ctkmsgbox(title="Cancel flight", message="Are you sure you want to cancel the flight!", icon="warning", option_1="Yes", option_2="No")
        if msg.get() != "Yes":
            return

        self.deleteRowPassengers(selected[0]) # passing flight id
            
        self.deleteRow()
        self.refresh()

    # database functions:
    def getRowsBookedFlights(self):
        date, time = str(datetime.now()).split()

        sql_cmd = f"SELECT Flight_ID, Airline, Place_of_departure, Destination, Class, Date, Time, Price FROM Flights NATURAL JOIN Passengers WHERE Name = '{appdata.data["user"]["name"]}' AND (Date > DATE('{date}') OR (Date = DATE('{date}') AND Time >= TIME('{time}')));"
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

        logger.info(f"{get_user_role[appdata.data["user"]["permission"]]}: {appdata.data["user"]["name"]} canceled flight with id {flight_id}")