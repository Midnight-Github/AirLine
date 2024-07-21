import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

class Flights(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root)

        self.root = root
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0,weight=1)

        style=ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background='#000000', foreground='white', relief='flat', rowheight=50)
        style.configure("Treeview", background='#333333', foreground='white', fieldbackground='#333333', rowheight=45)
        style.map('Treeview', background=[('selected','#D3D3D3')])

        self.flights_frame=ctk.CTkFrame(self,fg_color='transparent')
        self.flights_frame.grid(row=0,column=0,sticky='nesw')
        self.flights_frame.grid_rowconfigure(0, weight=1)
        self.flights_frame.grid_columnconfigure(0,weight=1)
        
        columns = ('airline', 'pod', 'dest', 'class', 'time', 'price')
        tree = ttk.Treeview(self.flights_frame, columns=columns, show='headings')
        tree.heading('airline', text='Airline')
        tree.column('airline',anchor='center', width=50)
        tree.heading('pod', text='Place of Departure')
        tree.column('pod',anchor='center', width=50)
        tree.heading('dest', text='Destination')
        tree.column('dest',anchor='center', width=50)
        tree.heading('class', text='Class')
        tree.column('class',anchor='center', width=50)
        tree.heading('time', text='Time')
        tree.column('time',anchor='center', width=50)
        tree.heading('price', text='Price')
        tree.column('price',anchor='center', width=50)
        
        flights = []
        flights.append(('Indigo','Delhi','Mumbai','Economy', '17:00 - 19:30' ,'5000INR'))
        flights.append(('Indigo','Bangalore','Mumbai','Economy', '18:00 - 20:00', '5500INR'))
        flights.append(('Emirates','Bangalore','Dubai','First Class', '01:00 - 04:30', '10000INR'))
        
        tree.tag_configure('oddrow', background='#333333')
        tree.tag_configure('evenrow', background='#1c1c1c')
        count=0
        for flight in flights:
            if count % 2 == 0:
                tree.insert('', tk.END, values=flight, tags=('oddrow',))
            else: 
                tree.insert('', tk.END, values=flight, tags=('evenrow',))
            count+=1
        
        tree.bind('<<TreeviewSelect>>')
        tree.grid(row=0, column=0, sticky='nsew')
        tree.grid_rowconfigure(0, weight=1)
        tree.grid_columnconfigure(0,weight=1)

        scrollbar = ttk.Scrollbar(self.flights_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')
 
        self.btn_frame=ctk.CTkFrame(self,fg_color='transparent')
        self.btn_frame.grid(row=1,column=0,sticky='se')
        self.back_btn = ctk.CTkButton(self.btn_frame, text="back", command=lambda : self.root.showFrame("Home"))
        self.back_btn.grid(row=0, column=1)
        self.add_btn = ctk.CTkButton(self.btn_frame, text="Add a Flight")
        self.add_btn.grid(row=0, column=0)
