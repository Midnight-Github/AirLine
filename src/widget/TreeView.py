import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

class TreeView(ctk.CTkFrame):
    def __init__(self, root, columns):
        super().__init__(root, fg_color="transparent")

        self.columns = columns

        self.row_count = 0

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("Treeview.Heading", background='#000000', foreground='white', relief='flat', rowheight=50)
        self.style.configure("Treeview", background='#333333', foreground='white', fieldbackground='#333333', rowheight=45)
        self.style.map('Treeview', background=[('selected','#D3D3D3')])

        self.tree = ttk.Treeview(self, columns=self.columns, show='headings')

        for column in self.columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, anchor='center', width=50)

        self.tree.tag_configure('oddrow', background='#333333')
        self.tree.tag_configure('evenrow', background='#1c1c1c')
        
        self.tree.bind('<<TreeviewSelect>>')
        self.tree.grid(row=0, column=0, sticky='nesw')

        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky='ns')

    def reloadTable(self, rows):
        self.deleteAllRows()

        for flight in rows:
            self.insertRow(flight)

    # tree view manipulation functions:
    def getSelectedRow(self):
        selected = self.tree.selection()
        if not selected:
            return None
        details = self.tree.item(selected[0])
        return details["values"]

    def insertRow(self, row):
        if self.row_count % 2 == 0:
            self.tree.insert('', tk.END, values=row, tags=('oddrow',)) # pyright: ignore
        else: 
            self.tree.insert('', tk.END, values=row, tags=('evenrow',)) # pyright: ignore

        self.row_count += 1
    
    def deleteRow(self):
        selected = self.tree.selection()[0]
        self.tree.delete(selected)

    def deleteAllRows(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.row_count = 0
