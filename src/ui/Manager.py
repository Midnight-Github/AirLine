import customtkinter as ctk
from ui.Home import Home
from ui.Login import Login
from ui.FrontPage import FrontPage
from ui.SignUp import SignUp

class Manager(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("700x500")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.page_class = {"Home": Home, "Login": Login, "FrontPage": FrontPage, "SignUp": SignUp}

        self.pages = dict()
        for frame_name, Frame in self.page_class.items():
            frame = Frame(self)
            frame.grid(row=0, column=0, sticky="nesw")
            self.pages[frame_name] = frame

        self.showFrame("FrontPage")

    def showFrame(self, frame):
        self.pages[frame].tkraise()

    def reinitFrame(self, frame):
        self.pages[frame].destroy()
        f = self.page_class[frame](self)
        f.grid(row=0, column=0, sticky="nesw")
        self.pages[frame] = f
