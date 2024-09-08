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

        self.date_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.date_frame.grid(row=4, column=0, padx=30, pady=15)
        self.fields["date_day"] = ctk.CTkEntry(self.date_frame, width=50, placeholder_text="DD", border_color="grey")
        self.fields["date_day"].grid(row=0, column=0, padx=5)
        self.divider = ctk.CTkLabel(self.date_frame, text='-', padx=5)
        self.divider.grid(row=0, column=1)
        self.fields["date_month"] = ctk.CTkEntry(self.date_frame, width=50, placeholder_text="MM", border_color="grey")
        self.fields["date_month"].grid(row=0, column=2, padx=5)
        self.divider = ctk.CTkLabel(self.date_frame, text='-', padx=5)
        self.divider.grid(row=0, column=3)
        self.fields["date_year"] = ctk.CTkEntry(self.date_frame, width=50, placeholder_text="YYYY", border_color="grey")
        self.fields["date_year"].grid(row=0, column=4, padx=5)

        self.time_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.time_frame.grid(row=5, column=0, padx=30, pady=15)
        self.fields["time_hour"] = ctk.CTkEntry(self.time_frame, width=50, placeholder_text="hh", border_color="grey")
        self.fields["time_hour"].grid(row=0, column=0, padx=5)
        self.divider = ctk.CTkLabel(self.time_frame, text=':', padx=5)
        self.divider.grid(row=0, column=1)
        self.fields["time_minute"] = ctk.CTkEntry(self.time_frame, width=50, placeholder_text="mm", border_color="grey")
        self.fields["time_minute"].grid(row=0, column=2, padx=5)
        self.divider = ctk.CTkLabel(self.time_frame, text=':', padx=5)
        self.divider.grid(row=0, column=3)
        self.fields["time_second"] = ctk.CTkEntry(self.time_frame, width=50, placeholder_text="ss", border_color="grey")
        self.fields["time_second"].grid(row=0, column=4, padx=5)

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
            "date": self.fields["date_year"].get() + '-' + self.fields["date_month"].get() + '-' + self.fields["date_day"].get(),
            "time": self.fields["time_hour"].get() + ':' + self.fields["time_minute"].get() + ':' + self.fields["time_second"].get(),
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
            self.fields["date_day"].configure(border_color="red")
            self.fields["date_month"].configure(border_color="red")
            self.fields["date_year"].configure(border_color="red")
            self.error_text.set("Invalid date")
            return False

        if re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d:[0-5]\d", target["time"]) is None:
            self.fields["time_hour"].configure(border_color="red")
            self.fields["time_minute"].configure(border_color="red")
            self.fields["time_second"].configure(border_color="red")
            self.error_text.set("Invalid time")
            return False

        try:
            price = int(target["price"])
        except ValueError:
            self.fields["price"].configure(border_color="red")
            self.error_text.set("Price should be a number")
            return False
        
        if price < 0:
            self.fields["price"].configure(border_color="red")
            self.error_text.set("Price should be a positive number")
            return False

        return True
