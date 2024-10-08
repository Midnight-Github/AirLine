import customtkinter as ctk
import tkinter as tk
from widget.BgFrame import BgFrame
from var.ConfigManager import server_config
from var.SqlManager import mysql
from reader.Logger import Logger
from var.Globals import get_user_role

logger = Logger(__name__).logger

class SignUp(BgFrame):
    def __init__(self, root):
        super().__init__(root, "login_bg.png", 1, 1)

        self.mysql = mysql

        self.content_frame = ctk.CTkFrame(self.bg_image_label, fg_color="transparent")
        self.content_frame.grid(row=0, column=0, sticky="ns")

        self.content_frame.grid_rowconfigure(0, weight=1)

        self.container_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.container_frame.grid(row=0, column=0)

        self.signup_frame = ctk.CTkFrame(self.container_frame, corner_radius=0, fg_color="transparent")
        self.signup_frame.grid(row=0, column=0, sticky="ns")
        self.signup_label = ctk.CTkLabel(self.signup_frame, text="Sign Up", font=ctk.CTkFont(size=30, weight="bold"))
        self.signup_label.grid(row=0, column=0, padx=30, pady=(0, 15), columnspan=2)

        self.username_entry = ctk.CTkEntry(self.signup_frame, width=200, placeholder_text="Username", border_color="grey")
        self.username_entry.grid(row=1, column=0, padx=30, pady=15, columnspan=2)
        self.password_entry = ctk.CTkEntry(self.signup_frame, width=200, show="*", placeholder_text="Password", border_color="grey")
        self.password_entry.grid(row=2, column=0, padx=30, pady=(0, 15), columnspan=2)
        self.confpassword_entry = ctk.CTkEntry(self.signup_frame, width=200, show="*", placeholder_text="Confirm password", border_color="grey")
        self.confpassword_entry.grid(row=3, column=0, padx=30, pady=(0, 15), columnspan=2)

        self.admin_check_box = ctk.CTkCheckBox(self.signup_frame, text="Admin", checkbox_width=17, checkbox_height=17, command=self.adminCheckboxEvent)
        self.admin_check_box.grid(row=4, column=0, sticky="nesw", padx=(40, 0), pady=(30, 0), columnspan=2)

        self.admin_password = ctk.CTkEntry(self.signup_frame, width=200, placeholder_text="Password", border_color="grey", show='*')
        self.admin_password.grid(row=5, column=0, padx=30, pady=15, columnspan=2)
        self.admin_password.grid_forget()

        self.signup_btn = ctk.CTkButton(self.signup_frame, text="Sign Up", command=self.SignUpEvent, width=100)
        self.signup_btn.grid(row=6, column=1, padx=(10, 30), pady=15, sticky="nesw")
        self.back_btn = ctk.CTkButton(self.signup_frame, text="Back",command=self.backEvent, width=100)
        self.back_btn.grid(row=6, column=0, padx=(30, 0), pady=15, sticky="nesw")

        self.error_text = tk.StringVar()
        self.error_label = ctk.CTkLabel(self.signup_frame, textvariable=self.error_text, font=ctk.CTkFont(size=15))
        self.error_label.grid(row=7, column=0, columnspan=2)

    def adminCheckboxEvent(self):
        if self.admin_check_box.get() == 1:
            self.admin_password.grid(row=5, column=0, padx=30, pady=15, columnspan=2)
        else:
            self.admin_password.grid_forget()

    def backEvent(self):    
        self.root.reinitFrame("SignUp")
        self.root.showFrame("FrontPage")

    def SignUpEvent(self):
        self.resetFields()

        input_username = self.username_entry.get()
        input_password = self.password_entry.get()
        input_confpassword = self.confpassword_entry.get()
        input_admin_password = self.admin_password.get()

        if not input_username:
            self.username_entry.configure(border_color="red")
            return
        if not input_password:
            self.password_entry.configure(border_color="red")
            return
        if not input_confpassword:
            self.confpassword_entry.configure(border_color="red")
            return

        if input_password != input_confpassword:
            self.error_text.set("Make sure the password is same")
            self.confpassword_entry.configure(border_color="red")
            self.password_entry.configure(border_color="red")
            return

        if self.admin_check_box.get() == 1 and not input_admin_password:
            self.admin_password.configure(border_color="red")
            return

        if input_username == "None":
            self.username_entry.configure(border_color="red")
            self.error_text.set("Username 'None' is not valid")
            return

        permission = 0
        if self.admin_check_box.get() == 1:
            if input_admin_password == server_config.data["admin"]["password"]:
                permission = 1
            else:
                self.error_text.set("Incorrect admin password")
                self.admin_password.configure(border_color="red")
                return

        sql_cmd = f"INSERT INTO Accounts VALUES('{input_username}', '{input_password}', {permission});"
        result = self.mysql.execute(sql_cmd)

        if result[0] is False:
            if f"Duplicate entry '{input_username}' for key 'accounts.PRIMARY'" == result[1].msg: # pyright: ignore
                self.error_text.set("Username already exists!")
                self.username_entry.configure(border_color="red")
                logger.warning("Failed to create an account as the username already exists")

            logger.error("Failed to create an account")
            logger.exception(result[1])
            return

        server_config.data["user"]["name"] = input_username
        server_config.data["user"]["permission"] = permission
        server_config.push()
        logger.info(f"{get_user_role[permission]}: {input_username} signed up")

        self.root.deleteFrameAll()
        self.root.showFrame("Home")

    def resetFields(self):
        self.username_entry.configure(border_color="grey")
        self.password_entry.configure(border_color="grey")
        self.confpassword_entry.configure(border_color="grey")
        self.admin_password.configure(border_color="grey")
