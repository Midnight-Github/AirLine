import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from var.ConfigManager import appdata
from reader.Logger import Logger
from var.SqlManager import mysql

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
        self.btn_frame.grid(row=2,column=0,sticky='se')
        self.back_btn = ctk.CTkButton(self.btn_frame, text="Back", command=lambda : self.root.showFrame("Home"))
        self.back_btn.grid(row=0, column=2, padx=5)
        self.refresh_btn = ctk.CTkButton(self.btn_frame, text="Refresh", command=self.refresh)
        self.refresh_btn.grid(row=0,column=3,sticky='se', padx=5)
    
    def refresh(self):
        logger.info("Refreshing Cart!")
        
        result = mysql.execute("SELECT * FROM Flights NATURAL JOIN Passengers;", buffered=True)
        if result[0] is False:
            logger.error("Failed to extract data from Passengers")
            logger.error(result[1])
            return

        logger.info("Extracted data from passengers")
        self.flights = self.formatFlights(result[1])

        # delete all rows here

        for count, flight in enumerate(self.cart):
            if count % 2 == 0:
                self.tree.insert('', tk.END, values=flight, tags=('oddrow',)) # pyright: ignore
            else: 
                self.tree.insert('', tk.END, values=flight, tags=('evenrow',)) # pyright: ignore
