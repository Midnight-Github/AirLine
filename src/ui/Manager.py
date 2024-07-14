import customtkinter as ctk
from var.Globals import appdata
from ui.Login import Login
from ui.FrontPage import FrontPage
from ui.SignUp import SignUp
from ui.Home import Home
from ui.Flights import Flights
from utils.Logger import Logger

logger = Logger(__name__).logger

class Manager(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("700x500")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame_class = {"Login": Login, "FrontPage": FrontPage, "SignUp": SignUp, "Home": Home, "Flights": Flights}

        self.frames = dict()
        for frame_name, Frame in self.frame_class.items():
            frame = Frame(self)
            frame.grid(row=0, column=0, sticky="nesw")
            self.frames[frame_name] = frame

        if appdata.data["user"]["name"] == "None":
            self.showFrame("FrontPage")
        else:
            self.showFrame("Home")
            
    def showFrame(self, frame):            
        self.frames[frame].tkraise()
        logger.info(f"Showing frame {frame}")

    def reinitFrame(self, frame):
        self.frames[frame].destroy()
        f = self.frame_class[frame](self)
        f.grid(row=0, column=0, sticky="nesw")
        self.frames[frame] = f
        logger.info(f"Reinitialized {frame}")

    def reinitFrameAll(self):
        for i in self.frame_class.keys():
            self.reinitFrame(i)
