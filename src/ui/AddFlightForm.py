import customtkinter as ctk
import tkinter as tk
import re
from datetime import datetime
from var.ConfigManager import config
from utils.ctkext import labeledComboBox
from datetime import datetime

class AddFlightForm(ctk.CTkToplevel):
    def __init__(self, submit_command):
        super().__init__()

        self.submit_command = submit_command

        self.resizable(False, False)
        self.title("Flight details")

        self.fields = dict()
        self.fields["airline"] = labeledComboBox(self, width=220, text="Airline", values=config.data["flight_info"]["flight_names"], row=0, column=0, padx=30, pady=10)
        self.fields["place_of_departure"] = labeledComboBox(self, width=220, text="place of departure", values=config.data["flight_info"]["states"], row=1, column=0, padx=30, pady=10)
        self.fields["destination"] = labeledComboBox(self, width=220, text="Destination", values=config.data["flight_info"]["states"], row=2, column=0, padx=30, pady=10)
        self.fields["class"] = labeledComboBox(self, width=220, text="Class", values=config.data["flight_info"]["flight_classes"], row=3, column=0, padx=30, pady=10)

        self.date_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.date_frame.grid(row=4, column=0, padx=30, pady=15, sticky='w')
        self.fields["date_day"] = labeledComboBox(self.date_frame, width=55, text="DD", values=[str(i) for i in range(1, 32)], row=0, column=0, padx=5, state="normal")
        self.divider = ctk.CTkLabel(self.date_frame, text='-', padx=5)
        self.divider.grid(row=0, column=1, sticky="s")
        self.fields["date_month"] = labeledComboBox(self.date_frame, width=55, text="MM", values=[str(i) for i in range(1, 13)], row=0, column=2, padx=5, state="normal")
        self.divider = ctk.CTkLabel(self.date_frame, text='-', padx=5)
        self.divider.grid(row=0, column=3, sticky="s")
        year = datetime.now().year
        self.fields["date_year"] = labeledComboBox(self.date_frame, width=70, text="YYYY", values=[str(i) for i in range(year, year + 20)], row=0, column=4, padx=5, state="normal")

        self.time_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.time_frame.grid(row=5, column=0, padx=30, pady=15, sticky='w')
        self.fields["time_hour"] = labeledComboBox(self.time_frame, width=55, text="hh", values=[str(i) for i in range(0, 24)], row=0, column=0, padx=5, state="normal")
        self.divider = ctk.CTkLabel(self.time_frame, text=':', padx=5)
        self.divider.grid(row=0, column=1, sticky="s")
        self.fields["time_minute"] = labeledComboBox(self.time_frame, width=55, text="mm", values=[str(i) for i in range(0, 60)], row=0, column=2, padx=5, state="normal")
        self.divider = ctk.CTkLabel(self.time_frame, text=':', padx=5)
        self.divider.grid(row=0, column=3, sticky="s")
        self.fields["time_second"] = labeledComboBox(self.time_frame, width=55, text="ss", values=[str(i) for i in range(0, 60)], row=0, column=4, padx=5, state="normal")

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
            if v.strip() == '' or v == "Empty":
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
