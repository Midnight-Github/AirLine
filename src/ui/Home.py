import customtkinter as ctk
from var.Globals import user_manager

class Home(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root)

        self.root = root

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.btn_frame = ctk.CTkFrame(self, fg_color="blue")
        self.btn_frame.grid(row=0, column=0)

        self.flights_btn = ctk.CTkButton(self.btn_frame, text="Flights", command=lambda : self.root.showFrame("Flights"))
        self.flights_btn.grid(row=0, column=0, pady=(0, 10))

        self.signout_btn = ctk.CTkButton(self.btn_frame, text="Sign out", command=self.signout)
        self.signout_btn.grid(row=1, column=0)

    def signout(self):
        user_manager.data["current"]["name"] = "None"
        user_manager.push()

        self.root.reinitFrameAll()
        self.root.showFrame("FrontPage")
