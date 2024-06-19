import customtkinter as ctk
import csv
from os import path
from template.Login import Login as login_template
from var.Globals import user_data_manager

class Login(login_template):
    def __init__(self, root):
        super().__init__(root)

        self.root = root

        self.content_frame.grid_rowconfigure(0, weight=1)

        self.container_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.container_frame.grid(row=0, column=0)

        self.login_frame = ctk.CTkFrame(self.container_frame, corner_radius=0, fg_color="transparent")
        self.login_frame.grid(row=0, column=0, sticky="ns")
        self.login_label = ctk.CTkLabel(self.login_frame, text="Login", font=ctk.CTkFont(size=30, weight="bold"))
        self.login_label.grid(row=0, column=0, padx=30, pady=(0, 15), columnspan=2)

        self.username_entry = ctk.CTkEntry(self.login_frame, width=200, placeholder_text="username")
        self.username_entry.grid(row=1, column=0, padx=30, pady=15, columnspan=2)

        self.password_entry = ctk.CTkEntry(self.login_frame, width=200, show="*", placeholder_text="password")
        self.password_entry.grid(row=2, column=0, padx=30, pady=(0, 15), columnspan=2)

        self.login_btn = ctk.CTkButton(self.login_frame, text="Login", command=self.loginEvent, width=100)
        self.login_btn.grid(row=3, column=1, padx=(10, 30), pady=15)
        self.back_btn = ctk.CTkButton(self.login_frame, text="Back", command=self.backEvent, width=100)
        self.back_btn.grid(row=3, column=0, padx=(30, 0), pady=15)

    def loginEvent(self):
        input_username = self.username_entry.get()
        input_password = self.password_entry.get()

        self.username_entry.configure(border_color="gray")
        self.password_entry.configure(border_color="gray")

        if not input_username:
            self.username_entry.configure(border_color="red")
            return
            
        if not input_password:
            self.password_entry.configure(border_color="red")
            return

        with open(path.dirname(__file__) + "//..//users//accounts.csv", mode="r") as f:
            reader = csv.reader(f)

            next(reader)
            for username, password, permission in reader:
                if input_username == username and input_password == password:
                    with open(path.dirname(__file__) + "\\..\\users\\user.toml", 'w') as f:
                        user_data_manager.data["current"]["name"] = input_username
                        user_data_manager.data["current"]["permission"] = permission
                        user_data_manager.data["current"]["signin"] = True
                        user_data_manager.push()
                    self.root.reinitFrame("Login")
                    self.root.showFrame("Home")
                    return

            self.username_entry.configure(border_color="red")
            self.password_entry.configure(border_color="red")
                    
    def backEvent(self):
        self.root.reinitFrame("Login")
        self.root.showFrame("FrontPage")