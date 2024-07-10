import customtkinter as ctk

class Flights(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root)

        self.root = root

        self.back_btn = ctk.CTkButton(self, text="back", command=lambda : self.root.showFrame("Home"))
        self.back_btn.grid(row=1, column=0)