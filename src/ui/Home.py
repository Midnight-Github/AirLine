import customtkinter as ctk
from var.Globals import user_manager
from template.Home import Home as home_template

class Home(home_template):
    def __init__(self, root):
        super().__init__(root)
