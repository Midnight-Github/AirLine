import customtkinter as ctk
import tkinter as tk
from ui.Home import Home
from ui.Login import Login

class Manager(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("700x500")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.page_class = {"Home": Home, "Login": Login}

        self.pages = dict()
        for frame_name, Frame in self.page_class.items():
            frame = Frame(self)
            frame.grid(row=0, column=0, sticky="nesw")
            self.pages[frame_name] = frame

        self.showFrame("Home")

    def showFrame(self, frame):
        self.pages[frame].tkraise()