import customtkinter as ctk
from var.ConfigManager import server_config
from reader.Logger import Logger
from var.SqlManager import mysql
from var.Globals import get_user_role
from widget.BgFrame import BgFrame
from CTkMessagebox import CTkMessagebox as ctkmsgbox

logger = Logger(__name__).logger

class Home(BgFrame):
    def __init__(self, root):
        super().__init__(root, "home_bg.png", 0.5, 0.3)

        self.mysql = mysql

        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky='n')

        self.welcome_label = ctk.CTkLabel(self.content_frame, text=f"Welcome {server_config.data["user"]["name"]}!", font=ctk.CTkFont(family="times new roman", size=30), fg_color="transparent")
        self.welcome_label.grid(row=0, column=0)

        self.btn_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.btn_frame.grid(row=1, column=0, pady=60)

        self.flights_btn = ctk.CTkButton(self.btn_frame, text="Flights", command=lambda : self.root.showFrame("Flights"))
        self.flights_btn.grid(row=0, column=0, pady=(0, 10))

        self.cart_btn = ctk.CTkButton(self.btn_frame, text="My flights", command=lambda : self.root.showFrame("Cart"))
        self.cart_btn.grid(row=1, column=0, pady=(0, 10))

        self.signout_btn = ctk.CTkButton(self.btn_frame, text="Sign out", command=self.signout)
        self.signout_btn.grid(row=2, column=0, pady=(0, 10))

        self.del_account_btn = ctk.CTkButton(self.btn_frame, text="Delete account", command=self.delAccount)
        self.del_account_btn.grid(row=3, column=0)

    def delAccount(self):
        msg = ctkmsgbox(title="Delete account", message="Are you sure you want to delete your account!", icon="question", option_1="Yes", option_2="No")
        if msg.get() != "Yes":
            return
        
        sql_cmd_del_passengers = f"DELETE FROM Passengers WHERE Name = '{server_config.data["user"]["name"]}';"
        sql_cmd_del_accounts = f"DELETE FROM Accounts WHERE Name = '{server_config.data["user"]["name"]}';"

        result_passengers = self.mysql.execute(sql_cmd_del_passengers)
        result_accounts = self.mysql.execute(sql_cmd_del_accounts)

        if result_passengers[0] is False:
            logger.error(f"Failed to delete {get_user_role[server_config.data["user"]["permission"]]}: {server_config.data["user"]["name"]}'s account")
            logger.error(result_passengers[1])
            return

        if result_accounts[0] is False:
            logger.error(f"Failed to delete {get_user_role[server_config.data["user"]["permission"]]}: {server_config.data["user"]["name"]}'s account")
            logger.error(result_accounts[1])
            return

        logger.info(f"Deleted {get_user_role[server_config.data["user"]["permission"]]}: {server_config.data["user"]["name"]}'s account")
        self.removeUserData()
        
        self.root.deleteFrameAll()
        self.root.showFrame("FrontPage")

    def signout(self):
        logger.info(f"{get_user_role[server_config.data["user"]["permission"]]}: {server_config.data["user"]["name"]} logged out")
        self.removeUserData()
        server_config.push()

        self.root.deleteFrameAll()
        self.root.showFrame("FrontPage")

    def removeUserData(self):
        server_config.data["user"]["name"] = "None"
        server_config.data["user"]["permission"] = -1
        server_config.data["user"]["show_flights_by"] = "available"
        server_config.push()