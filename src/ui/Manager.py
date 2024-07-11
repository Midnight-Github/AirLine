import customtkinter as ctk
from var.Globals import user_manager
from ui.Login import Login
from ui.FrontPage import FrontPage
from ui.SignUp import SignUp
from ui.Home import Home
from ui.Flights import Flights
from ui.SideBar import SideBar

class Manager(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("700x500")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.frame_class = {"Login": Login, "FrontPage": FrontPage, "SignUp": SignUp, "Home": Home, "Flights": Flights, "SideBar": SideBar}
        self.sidebar_supporting_pages = ("Home", "Flights")

        self.frames = dict()
        for frame_name, Frame in self.frame_class.items():
            frame = Frame(self)
            frame.grid(row=0, column=1, sticky="nesw")
            self.frames[frame_name] = frame

        if user_manager.data["current"]["name"].lower() == "none":
            self.showFrame("FrontPage")
        else:
            self.showFrame("Home")
            
    def showFrame(self, frame):
        if frame == 'SideBar':
            raise ValueError("Cannot raise SideBar")
            
        self.frames[frame].tkraise()

        if frame in self.sidebar_supporting_pages:
            self.frames['SideBar'].grid(row=0, column=0, sticky="nesw")
        else:
            self.frames['SideBar'].grid_forget()

    def reinitFrame(self, frame):
        self.frames[frame].destroy()
        f = self.frame_class[frame](self)
        if frame != 'SideBar':
            f.grid(row=0, column=1, sticky="nesw")
        self.frames[frame] = f

    def reinitFrameAll(self):
        for i in self.frame_class.keys():
            self.reinitFrame(i)
