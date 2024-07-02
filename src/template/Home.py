import customtkinter as ctk
from var.Globals import user_data_manager

class Home(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root)

        self.root = root

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.grid(row=0, column=1, sticky="nesw")

        self.flights_btn = ctk.CTkButton(self.btn_frame, text="Flights", command=lambda : self.root.showFrame("Flights"))
        self.flights_btn.grid(row=0, column=0, pady=(0, 10))

        self.side_bar = ctk.CTkFrame(self, fg_color="blue")
        self.side_bar.grid(row=0, column=0, sticky="nesw")
        self.signout_btn = ctk.CTkButton(self.side_bar, text="Sign out", command=self.signOut)
        self.signout_btn.grid(row=0, column=0)

    def signOut(self):
        user_data_manager.data["current"]["name"] = False
        user_data_manager.push()
        self.side_bar.destroy()

        self.root.reinitFrameAll()

        self.root.showFrame("FrontPage")