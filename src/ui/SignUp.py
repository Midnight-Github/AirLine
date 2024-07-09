import customtkinter as ctk
import tkinter as tk
from os import path
from template.Login import Login as signup_template
import csv
from var.Globals import user_manager

class SignUp(signup_template):
    def __init__(self, root):
        super().__init__(root)

        self.root = root

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

        self.signup_btn = ctk.CTkButton(self.signup_frame, text="Sign Up", command=self.SignUpEvent, width=100)
        self.signup_btn.grid(row=4, column=1, padx=(10, 30), pady=15)
        self.back_btn = ctk.CTkButton(self.signup_frame, text="Back",command=self.backEvent, width=100)
        self.back_btn.grid(row=4, column=0, padx=(30, 0), pady=15)

        self.error_text = tk.StringVar()
        self.error_label = ctk.CTkLabel(self.signup_frame, textvariable=self.error_text, font=ctk.CTkFont(size=15))
        self.error_label.grid(row=5, column=0, columnspan=2)

    def backEvent(self):    
        self.root.reinitFrame("SignUp")
        self.root.showFrame("FrontPage")

    def SignUpEvent(self):
        self.resetFields()

        if not self.username_entry.get():
            self.username_entry.configure(border_color="red")
            return
        if not self.password_entry.get():
            self.password_entry.configure(border_color="red")
            return
        if not self.confpassword_entry.get():
            self.confpassword_entry.configure(border_color="red")
            return

        if self.password_entry.get() != self.confpassword_entry.get():
            self.error_text.set("Make sure the password is same")
            return

        with open(path.dirname(__file__)+"\\..\\users\\accounts.csv",'r+', newline='')as accounts:
            reader=csv.reader(accounts)
            next(reader)
            for username, _, _ in reader:
                if self.username_entry.get() == username:
                    self.error_text.set("Username already exists")
                    return

            writer = csv.writer(accounts)
            writer.writerow([self.username_entry.get(), self.password_entry.get(), 0]) # permission is 0 for now

        user_manager.data["current"]["name"] = self.username_entry.get()
        user_manager.data["current"]["permission"] = 0
        user_manager.push()

        self.root.showFrame("Home")

    def resetFields(self):
        self.username_entry.configure(border_color="grey")
        self.password_entry.configure(border_color="grey")
        self.confpassword_entry.configure(border_color="grey")
