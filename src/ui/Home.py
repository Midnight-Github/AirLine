import customtkinter as ctk
from var.ConfigManager import appdata
from reader.Logger import Logger
from var.SqlManager import mysql
from var.Globals import get_user_position

logger = Logger(__name__).logger

class Home(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root)

        self.root = root
        self.mysql = mysql

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.btn_frame = ctk.CTkFrame(self, fg_color="blue")
        self.btn_frame.grid(row=0, column=0)

        self.flights_btn = ctk.CTkButton(self.btn_frame, text="Flights", command=lambda : self.root.showFrame("Flights"))
        self.flights_btn.grid(row=0, column=0, pady=(0, 10))

        self.signout_btn = ctk.CTkButton(self.btn_frame, text="Sign out", command=self.signout)
        self.signout_btn.grid(row=1, column=0)

        self.del_account_btn = ctk.CTkButton(self.btn_frame, text="Delete account", command=self.delAccount)
        self.del_account_btn.grid(row=2, column=0)

    def signout(self):
        logger.info(f"{get_user_position[appdata.data["user"]["permission"]]}: {appdata.data["user"]["name"]} logged out")
        appdata.data["user"]["name"] = "None"
        appdata.data["user"]["permission"] = -1
        appdata.push()

        self.root.reinitFrameAll()
        self.root.showFrame("FrontPage")

    def delAccount(self):
        sql_cmd = "DELETE FROM Accounts WHERE Name = %s"
        sql_args = (appdata.data["user"]["name"],)
        success, result = self.mysql.execute(sql_cmd, sql_args)
        if success:
            logger.info(f"Deleted {get_user_position[appdata.data["user"]["permission"]]}: {appdata.data["user"]["name"]}'s account")
            appdata.data["user"]["name"] = "None"
            appdata.data["user"]["permission"] = -1
            appdata.push()
            self.root.reinitFrameAll()
            self.root.showFrame("FrontPage")
        else:
            logger.error(f"Failed to delete {get_user_position[appdata.data["user"]["permission"]]}: {appdata.data["user"]["name"]}'s account")
            logger.exception(result)