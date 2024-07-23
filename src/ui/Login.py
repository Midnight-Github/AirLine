import customtkinter as ctk
import csv
from os import path
from template.Login import Login as login_template
from var.ConfigManager import appdata
from var.SqlManager import mysql
from reader.Logger import Logger
from var.Globals import get_user_position

logger = Logger(__name__).logger

class Login(login_template):
    def __init__(self, root):
        super().__init__(root)

        self.root = root
        self.mysql = mysql

        self.content_frame.grid_rowconfigure(0, weight=1)

        self.container_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.container_frame.grid(row=0, column=0)

        self.login_frame = ctk.CTkFrame(self.container_frame, corner_radius=0, fg_color="transparent")
        self.login_frame.grid(row=0, column=0, sticky="ns")
        self.login_label = ctk.CTkLabel(self.login_frame, text="Login", font=ctk.CTkFont(size=30, weight="bold"))
        self.login_label.grid(row=0, column=0, padx=30, pady=(0, 15), columnspan=2)

        self.username_entry = ctk.CTkEntry(self.login_frame, width=200, placeholder_text="username", border_color="grey")
        self.username_entry.grid(row=1, column=0, padx=30, pady=15, columnspan=2)
        self.password_entry = ctk.CTkEntry(self.login_frame, width=200, show="*", placeholder_text="password", border_color="grey")
        self.password_entry.grid(row=2, column=0, padx=30, pady=(0, 15), columnspan=2)

        self.login_btn = ctk.CTkButton(self.login_frame, text="Login", command=self.loginEvent, width=100)
        self.login_btn.grid(row=3, column=1, padx=(10, 30), pady=15)
        self.back_btn = ctk.CTkButton(self.login_frame, text="Back", command=self.backEvent, width=100)
        self.back_btn.grid(row=3, column=0, padx=(30, 0), pady=15)

    def loginEvent(self):
        self.resetFields()

        input_username = self.username_entry.get()
        input_password = self.password_entry.get()

        if not input_username:
            self.username_entry.configure(border_color="red")
            return
            
        if not input_password:
            self.password_entry.configure(border_color="red")
            return

        sql_cmd = "SELECT Name, Password, Permission FROM Accounts WHERE Name = %s AND Password = %s"
        sql_args = (input_username, input_password)

        success, result = self.mysql.execute(sql_cmd, sql_args, buffered=True)
        if success:
            if result:
                appdata.data["user"]["name"] = input_username
                appdata.data["user"]["permission"] = result[0][2] #pyright: ignore
                appdata.push()
                logger.info(f"{get_user_position[result[0][2]]}: {input_username} logged in") #pyright: ignore
                self.root.showFrame("Home")
                return
        else:
            logger.error("Failed to verify user")
            logger.exception(result)

        self.username_entry.configure(border_color="red")
        self.password_entry.configure(border_color="red")
        logger.warning(f"{input_username} tried to login but failed")

    def resetFields(self):
        self.username_entry.configure(border_color="gray")
        self.password_entry.configure(border_color="gray")
                    
    def backEvent(self):
        self.root.reinitFrame("Login")
        self.root.showFrame("FrontPage")