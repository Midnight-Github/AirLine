import customtkinter as ctk
from template.TreeView import TreeView

class ShowPassengers(ctk.CTkToplevel):
    def __init__(self, flight_id):
        super().__init__()
        
        self.resizable(False, False)
        self.title("Passengers")
        
        self.tree_view = TreeView(self, heading="Passengers", columns=("Passengers",))
        self.tree_view.grid(row=0, column=0)
        
        
