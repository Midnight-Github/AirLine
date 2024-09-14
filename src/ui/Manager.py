import customtkinter as ctk
from var.ConfigManager import server_config
from ui.Login import Login
from ui.FrontPage import FrontPage
from ui.SignUp import SignUp
from ui.Home import Home
from ui.Flights import Flights
from ui.Cart import Cart
from reader.Logger import Logger

logger = Logger(__name__).logger

class Manager(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("700x530")
        self.title("Airline")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame_class = {"Login": Login, "FrontPage": FrontPage, "SignUp": SignUp, "Home": Home, "Flights": Flights, "Cart": Cart}

        self.frames = dict.fromkeys(self.frame_class.keys())

        if server_config.data["user"]["name"] == "None":
            self.showFrame("FrontPage")
        else:
            self.showFrame("Home")
            
    def showFrame(self, frame):
        if self.frames[frame] is None:
            self.initFrame(frame)
            
        self.frames[frame].tkraise() # pyright: ignore
        logger.info(f"Showing {frame}")

    def initFrame(self, frame):
        f = self.frame_class[frame](self)
        f.grid(row=0, column=0, sticky="nesw")
        self.frames[frame] = f
        logger.info(f"Initialized {frame}")

    def deleteFrame(self, frame):
        if self.frames[frame] is None:
            return

        self.frames[frame].destroy() # pyright: ignore
        self.frames[frame] = None
        logger.info(f"Deleted {frame}")

    def deleteFrameAll(self):
        for i in self.frame_class.keys():
            self.deleteFrame(i)

    def reinitFrame(self, frame):
        self.deleteFrame(frame)
        self.initFrame(frame)

    def reinitFrameAll(self):
        for i in self.frame_class.keys():
            self.reinitFrame(i)
