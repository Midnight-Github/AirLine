import customtkinter as ctk
from var.Globals import user_manager

class Home(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root)

        self.root = root

        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.grid(row=0, column=1, sticky="nesw")

        self.flights_btn = ctk.CTkButton(self.btn_frame, text="Flights", command=lambda : self.root.showFrame("Flights"))
        self.flights_btn.grid(row=0, column=0, pady=(0, 10))
