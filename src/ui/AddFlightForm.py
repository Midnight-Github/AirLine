import customtkinter as ctk
import tkinter as tk
import re
from datetime import datetime

class AddFlightForm(ctk.CTkToplevel):
    def __init__(self, submit_command):
        super().__init__()

        self.submit_command = submit_command

        self.resizable(False, False)
        self.title("Flight details")

        self.fields = dict()

        self.fields["airline"] = ctk.CTkEntry(self, width=200, placeholder_text="Airline", border_color="grey")
        self.fields["airline"].grid(row=0, column=0, padx=30, pady=(30, 15))
        self.fields["place_of_departure"] = ctk.CTkEntry(self, width=200, placeholder_text="place of departure", border_color="grey")
        self.fields["place_of_departure"].grid(row=1, column=0, padx=30, pady=15)
        self.fields["destination"] = ctk.CTkEntry(self, width=200, placeholder_text="Destination", border_color="grey")
        self.fields["destination"].grid(row=2, column=0, padx=30, pady=15)
        self.fields["class"] = ctk.CTkEntry(self, width=200, placeholder_text="Class", border_color="grey")
        self.fields["class"].grid(row=3, column=0, padx=30, pady=15)
        self.fields["date"] = ctk.CTkEntry(self, width=200, placeholder_text="Date: YYYY-MM-DD", border_color="grey")
        self.fields["date"].grid(row=4, column=0, padx=30, pady=15)
        self.fields["time"] = ctk.CTkEntry(self, width=200, placeholder_text="Time: hh:mm:ss", border_color="grey")
        self.fields["time"].grid(row=5, column=0, padx=30, pady=15)
        self.fields["price"] = ctk.CTkEntry(self, width=200, placeholder_text="Price", border_color="grey")
        self.fields["price"].grid(row=6, column=0, padx=30, pady=15)

        self.error_text = tk.StringVar()
        self.error_label = ctk.CTkLabel(self, textvariable=self.error_text, font=ctk.CTkFont(size=15))
        self.error_label.grid(row=7, column=0)

        self.submit_btn = ctk.CTkButton(self, text="Submit", command=self.submit)
        self.submit_btn.grid(row=8, column=0, padx=30, pady=15, sticky="e")
        
    def submit(self):
        for i in self.fields.values():
            i.configure(border_color="grey")

        details = {
            "airline": self.fields["airline"].get(),
            "place_of_departure": self.fields["place_of_departure"].get(),
            "destination": self.fields["destination"].get(),
            "class": self.fields["class"].get(),
            "date": self.fields["date"].get(),
            "time": self.fields["time"].get(),
            "price": self.fields["price"].get()
        }

        if self.verification(details) is False:
            return

        self.submit_command(details)

    def verification(self, target):
        for i, v in target.items():
            if v.strip() == '':
                self.fields[i].configure(border_color="red")
                self.error_text.set("All fields must be filled")
                return False
            
        try:
            bool(datetime.strptime(target["date"], "%Y-%m-%d"))
        except ValueError:
            self.fields["date"].configure(border_color="red")
            self.error_text.set("Invalid date")
            return False

        if re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d:[0-5]\d", target["time"]) is None:
            self.fields["time"].configure(border_color="red")
            self.error_text.set("Invalid time")
            return False

        try:
            int(target["price"])
        except ValueError:
            self.error_text.set("Price should be a number")
            return False

        return True