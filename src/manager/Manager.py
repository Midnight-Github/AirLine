import customtkinter as ctk
from var.Globals import user_data_manager
from authentication.Login import Login
from authentication.FrontPage import FrontPage
from authentication.SignUp import SignUp
from home.Home import Home
from home.Flights import Flights

class Manager(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("700x500")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.page_class = {"Login": Login, "FrontPage": FrontPage, "SignUp": SignUp, "Home": Home, "Flights": Flights}

        self.pages = dict()
        for frame_name, Frame in self.page_class.items():
            frame = Frame(self)
            frame.grid(row=0, column=0, sticky="nesw")
            self.pages[frame_name] = frame

        if user_data_manager.data["current"]["name"] == False:
            self.showFrame("FrontPage")
        else:
            self.showFrame("Home")
            
    def showFrame(self, frame):
        self.pages[frame].tkraise()

    def reinitFrame(self, frame):
        self.pages[frame].destroy()
        f = self.page_class[frame](self)
        f.grid(row=0, column=0, sticky="nesw")
        self.pages[frame] = f

    def reinitFrameAll(self):
        for i in self.page_class.keys():
            self.reinitFrame(i)
