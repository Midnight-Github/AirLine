import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from var.ConfigManager import appdata
from reader.Logger import Logger
from var.SqlManager import mysql
from var.Globals import get_user_role
from CTkMessagebox import CTkMessagebox as ctkmsgbox
from datetime import datetime

logger = Logger(__name__).logger

class Cart(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root)

        self.root = root
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0,weight=1)

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("Treeview.Heading", background='#000000', foreground='white', relief='flat', rowheight=50)
        self.style.configure("Treeview", background='#333333', foreground='white', fieldbackground='#333333', rowheight=45)
        self.style.map('Treeview', background=[('selected','#D3D3D3')])
        
        self.header = ctk.CTkLabel(self, text="Booked Flights", font=ctk.CTkFont(size=30, weight="bold"))
        self.header.grid(row=0, column=0, sticky='new')
        
        self.columns = ('id', 'airline', 'pod', 'dest', 'class', 'date', 'time', 'price')
        self.tree = ttk.Treeview(self, columns=self.columns, show='headings')
        self.tree.heading('id', text='ID')
        self.tree.column('id', anchor='center', width=50)
        self.tree.heading('airline', text='Airline')
        self.tree.column('airline',anchor='center', width=50)
        self.tree.heading('pod', text='Place of Departure')
        self.tree.column('pod',anchor='center', width=50)
        self.tree.heading('dest', text='Destination')
        self.tree.column('dest',anchor='center', width=50)
        self.tree.heading('class', text='Class')
        self.tree.column('class',anchor='center', width=50)
        
        self.tree.heading('date', text='Date')
        self.tree.column('date',anchor='center', width=50)
        
        self.tree.heading('time', text='Time')
        self.tree.column('time',anchor='center', width=50)
        self.tree.heading('price', text='Price')
        self.tree.column('price',anchor='center', width=50)
        
        self.tree.tag_configure('oddrow', background='#333333')
        self.tree.tag_configure('evenrow', background='#1c1c1c')
        
        self.tree.bind('<<TreeviewSelect>>')
        self.tree.grid(row=1, column=0, sticky='nesw')

        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=1, column=1, sticky='ns')

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
        date, time = str(datetime.now()).split()

        sql_cmd = f"SELECT * FROM Flights NATURAL JOIN Passengers WHERE Name = '{appdata.data["user"]["name"]}' AND (Date > DATE('{date}') OR (Date = DATE('{date}') AND Time >= TIME('{time}')));"
        result = mysql.execute(sql_cmd, buffered=True)

        if result[0] is False:
            logger.error("Failed to extract data from Passengers")
            logger.error(result[1])
            return

        logger.info("Extracted data from passengers")
        self.flights = self.formatFlights(result[1])

        self.deleteAllRows()

        for count, flight in enumerate(self.flights):
            if count % 2 == 0:
                self.tree.insert('', tk.END, values=flight, tags=('oddrow',)) # pyright: ignore
            else: 
                self.tree.insert('', tk.END, values=flight, tags=('evenrow',)) # pyright: ignore

    def formatFlights(self, table):
        for i, row in enumerate(table):
            row = row[:-1] + (str(row[-1]) + 'INR',)
            table[i] = row
        return table

    def deleteAllRows(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

    def cancelFlight(self):
        selected = self.getSelectedFlight()
        if selected is None:
            ctkmsgbox(title="Cancel flight", message="No flight selected!")
            return

        msg = ctkmsgbox(title="Cancel flight", message="Are you sure you want to cancel the flight!", icon="warning", option_1="Yes", option_2="No")
        if msg.get() != "Yes":
            return

        if self.deleteRowPassengers(selected[0]) is False:
            return
            
        selected = self.tree.selection()[0]
        self.tree.delete(selected)

    def deleteRowPassengers(self, flight_id):
        sql_cmd_del_passengers = f"DELETE FROM Passengers WHERE Flight_ID = {flight_id};"
        result = mysql.execute(sql_cmd_del_passengers)

        if result[0] is False:
            logger.error("Failed to delete data from Passengers!")
            logger.error(result[1])
            return False

        logger.info(f"{get_user_role[appdata.data["user"]["permission"]]}: {appdata.data["user"]["name"]} canceled flight with id {flight_id}")

    def getSelectedFlight(self):
        selected = self.tree.selection()
        if not selected:
            return None
        details = self.tree.item(selected[0])
        return details["values"]