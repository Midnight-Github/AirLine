import customtkinter as ctk
import tkinter as tk
from os import path
from PIL import Image
from template.Login import Login as signup_template
import csv


class SignUp(signup_template):
    def __init__(self, root):
        super().__init__(root)

        self.root = root

        self.content_frame.grid_rowconfigure(0,weight=1)

        self.container_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.container_frame.grid(row=0, column=0)

        self.signup_frame = ctk.CTkFrame(self.container_frame, corner_radius=0, fg_color="transparent")
        self.signup_frame.grid(row=0, column=0, sticky="ns")
        self.signup_label = ctk.CTkLabel(self.signup_frame, text="Sign Up",
                                                    font=ctk.CTkFont(size=30, weight="bold"))
        self.signup_label.grid(row=0, column=0, padx=30, pady=(0, 15), columnspan=2)
        self.username_entry = ctk.CTkEntry(self.signup_frame, width=200, placeholder_text="username")
        self.username_entry.grid(row=1, column=0, padx=30, pady=15, columnspan=2)
        self.password_entry = ctk.CTkEntry(self.signup_frame, width=200, show="*", placeholder_text="password")
        self.password_entry.grid(row=2, column=0, padx=30, pady=(0, 15), columnspan=2)
        self.confpassword_entry = ctk.CTkEntry(self.signup_frame, width=200, show="*", placeholder_text="confirm password")
        self.confpassword_entry.grid(row=3, column=0, padx=30, pady=(0, 15), columnspan=2)
        self.signup_btn = ctk.CTkButton(self.signup_frame, text="Sign Up", command=self.SignUpEvent, width=100)
        self.signup_btn.grid(row=4, column=1, padx=(10, 30), pady=15)
        self.back_btn = ctk.CTkButton(self.signup_frame, text="Back",command=self.backEvent, width=100)
        self.back_btn.grid(row=4, column=0, padx=(30, 0), pady=15)

    def backEvent(self):    
        self.root.showFrame("Home")

    def SignUpEvent(self):
        with open(path.dirname(__file__)+"\\..\\users\\accounts.csv",'r+')as accounts:
            reader=csv.reader(accounts)
            next(reader)
            if next(reader) == None:
                for username,password in reader:
                    if self.username_entry.get()==username:
                        self.username_exist=ctk.CTkLabel(self.signup_frame, text="Username already exists", 
                                                        font=ctk.CTkFont(size=15))
                        self.username_exist.grid(row=5,column=0, columnspan=2)
                        return
            writer=csv.writer(accounts)
            if self.username_entry.get() and self.password_entry.get() and self.confpassword_entry.get() != None:
                if self.password_entry.get()==self.confpassword_entry.get():
                    writer.writerow([self.username_entry.get(),self.password_entry.get()])
                elif self.password_entry.get() != self.confpassword_entry.get():
                    self.password_err=ctk.CTkLabel(self.signup_frame, text="Make sure the password is same", 
                                                     font=ctk.CTkFont(size=15))
                    self.password_err.grid(row=5,column=0, columnspan=2)
            else:
                self.username_entry.configure(border_width=1,border_color='red')
