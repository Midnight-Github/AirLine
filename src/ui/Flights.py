import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from var.ConfigManager import appdata

class Flights(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root)

        self.root = root
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0,weight=1)

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("Treeview.Heading", background='#000000', foreground='white', relief='flat', rowheight=50)
        self.style.configure("Treeview", background='#333333', foreground='white', fieldbackground='#333333', rowheight=45)
        self.style.map('Treeview', background=[('selected','#D3D3D3')])

        self.flights_frame = ctk.CTkFrame(self,fg_color='transparent')
        self.flights_frame.grid(row=0,column=0,sticky='nesw')
        self.flights_frame.grid_rowconfigure(0, weight=1)
        self.flights_frame.grid_columnconfigure(0,weight=1)
        
        self.columns = ('airline', 'pod', 'dest', 'class', 'time', 'price')
        self.tree = ttk.Treeview(self.flights_frame, columns=self.columns, show='headings')
        self.tree.heading('airline', text='Airline')
        self.tree.column('airline',anchor='center', width=50)
        self.tree.heading('pod', text='Place of Departure')
        self.tree.column('pod',anchor='center', width=50)
        self.tree.heading('dest', text='Destination')
        self.tree.column('dest',anchor='center', width=50)
        self.tree.heading('class', text='Class')
        self.tree.column('class',anchor='center', width=50)
        self.tree.heading('time', text='Time')
        self.tree.column('time',anchor='center', width=50)
        self.tree.heading('price', text='Price')
        self.tree.column('price',anchor='center', width=50)
        
        self.flights = []
        self.flights.append(('Indigo','Delhi','Mumbai','Economy', '17:00 - 19:30' ,'5000INR'))
        self.flights.append(('Indigo','Bangalore','Mumbai','Economy', '18:00 - 20:00', '5500INR'))
        self.flights.append(('Emirates','Bangalore','Dubai','First Class', '01:00 - 04:30', '10000INR'))
        
        self.tree.tag_configure('oddrow', background='#333333')
        self.tree.tag_configure('evenrow', background='#1c1c1c')

        count=0
        for flight in self.flights:
            if count % 2 == 0:
                self.tree.insert('', tk.END, values=flight, tags=('oddrow',))
            else: 
                self.tree.insert('', tk.END, values=flight, tags=('evenrow',))
            count+=1
        
        self.tree.bind('<<TreeviewSelect>>')
        self.tree.grid(row=0, column=0, sticky='nsew')
        self.tree.grid_rowconfigure(0, weight=1)
        self.tree.grid_columnconfigure(0,weight=1)

        self.scrollbar = ttk.Scrollbar(self.flights_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky='ns')

        self.btn_frame = ctk.CTkFrame(self,fg_color='transparent')
        self.btn_frame.grid(row=1,column=0,sticky='se')
        self.back_btn = ctk.CTkButton(self.btn_frame, text="back", command=lambda : self.root.showFrame("Home"))
        self.back_btn.grid(row=0, column=1)

        if appdata.data["user"]["permission"] > 0:
            self.add_btn = ctk.CTkButton(self.btn_frame, text="Add a Flight")
            self.add_btn.grid(row=0, column=0)
