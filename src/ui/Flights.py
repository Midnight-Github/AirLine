import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from var.ConfigManager import appdata
from reader.Logger import Logger
from var.SqlManager import mysql
from ui.AddFlight import AddFlight
from var.Globals import get_user_position
from CTkMessagebox import CTkMessagebox as ctkmsgbox

logger = Logger(__name__).logger

class Flights(ctk.CTkFrame):
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
        
        self.header = ctk.CTkLabel(self, text="Available Flights", font=ctk.CTkFont(size=30, weight="bold"))
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
        
        self.extractFlights()

        # ('Indigo','Delhi','Mumbai','Economy', '17:00 - 19:30' ,'5000INR')
        # ('Indigo','Bangalore','Mumbai','Economy', '18:00 - 20:00', '5500INR')
        # ('Emirates','Bangalore','Dubai','First Class', '01:00 - 04:30', '10000INR')
        
        self.tree.tag_configure('oddrow', background='#333333')
        self.tree.tag_configure('evenrow', background='#1c1c1c')
        
        self.tree.bind('<<TreeviewSelect>>')
        self.tree.grid(row=1, column=0, sticky='nesw')

        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=1, column=1, sticky='ns')

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
        selected = self.getSelectedFlight()
        if selected is None:
            return
        if self.deleteRowFlights(selected[0]) is False:
            return
        selected = self.tree.selection()[0]
        self.tree.delete(selected)
        
    def deleteAllRows(self):
            for row in self.tree.get_children():
                self.tree.delete(row)

    def getSelectedFlight(self):
        selected = self.tree.selection()
        if not selected:
            return None
        details = self.tree.item(selected[0])
        return details["values"]

    def refresh(self):
        logger.info("Refreshing Flights!")
        self.extractFlights()

    def extractFlights(self):
        result = mysql.execute("SELECT * FROM Flights;", buffered=True)
        if result[0] is False:
            logger.error("Failed to extract data from Flights!")
            logger.error(result[1])
            return

        logger.info("Extracted data from flights")
        self.flights = self.formatFlights(result[1])

        # delete all rows here

        for count, flight in enumerate(self.flights):
            if count % 2 == 0:
                self.tree.insert('', tk.END, values=flight, tags=('oddrow',)) # pyright: ignore
            else: 
                self.tree.insert('', tk.END, values=flight, tags=('evenrow',)) # pyright: ignore

    def insertRowFlights(self, sql_args):
        sql_cmd = "INSERT INTO Flights (Airline, Pod, Destination, Class, Date, Time, Price) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        result = mysql.execute(sql_cmd, sql_args)
        if result[0] is False:
            logger.error("Failed to insert data to Flights!")
            logger.error(result[1])
            return False

        logger.info(f"Inserted {sql_args} to Flights")
        if self.isAddFlightFormAlive():
            self.add_flight_form.destroy() # pyright: ignore
            self.add_flight_form.update() # pyright: ignore

        self.extractFlights()
        return True

    def deleteRowFlights(self, flight_id):
        sql_cmd = "DELETE FROM Flights WHERE Flight_ID = %s;"
        result = mysql.execute(sql_cmd, (flight_id,))
        if result[0] is False:
            logger.error("Failed to delete data from Flights!")
            logger.error(result[1])
            return False

        logger.info(f"Deleted flight with id {flight_id} from Flights")
        return True
    
    def BookFlight(self):
        flight_id = self.getSelectedFlight()[0]
        result = mysql.execute(f"INSERT INTO Passengers VALUES(\"{appdata.data["user"]["name"]}\",{flight_id});")
        if result[0] is False:
            ctkmsgbox(title="Flights", message="You have already booked this flight")
            logger.error("Failed to insert data to Passengers!")
            logger.error(result[1])
            return
        
        ctkmsgbox(message="Successfully booked flight",icon="check")
        logger.info(f"Booked Flight with flight id: {flight_id} for {get_user_position[appdata.data["user"]["permission"]]}: {appdata.data["user"]["name"]}")
        self.flights = self.formatFlights(result[1])
