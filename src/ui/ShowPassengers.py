import customtkinter as ctk
from widget.TreeView import TreeView
from var.SqlManager import mysql

class ShowPassengers(ctk.CTkToplevel):
    def __init__(self, flight_id):
        super().__init__()

        self.flight_id = flight_id

        self.grid_rowconfigure(0, weight=10)
        self.grid_columnconfigure(0,weight=10)

        self.minsize(300, 500)
        self.resizable(False, False)
        self.title("Passengers")
        
        self.tree_view = TreeView(self, columns=("Passengers",))
        self.tree_view.grid(row=0, column=0, sticky="nesw")

        self.refresh_btn = ctk.CTkButton(self, text="Refresh", command=self.fillTable)
        self.refresh_btn.grid(row=1, column=0)

        self.fillTable()
        
    def fillTable(self):
        result = mysql.execute(f"SELECT Name FROM Passengers WHERE Flight_ID = {self.flight_id};", buffered=True)
        if result[0] is False:
            return

        self.tree_view.reloadTable(result[1])
