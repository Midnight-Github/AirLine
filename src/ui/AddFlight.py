import customtkinter as ctk
import tkinter as tk

class AddFlight(ctk.CTkToplevel):
    def __init__(self, submit_command):
        super().__init__()

        self.submit_command = submit_command

        self.resizable(False, False)
        self.title("Flight details")

        self.airline_entry = ctk.CTkEntry(self, width=200, placeholder_text="Airline", border_color="grey")
        self.airline_entry.grid(row=0, column=0, padx=30, pady=(30, 15))
        self.pod_entry = ctk.CTkEntry(self, width=200, placeholder_text="Place of departure", border_color="grey")
        self.pod_entry.grid(row=1, column=0, padx=30, pady=15)
        self.destination_entry = ctk.CTkEntry(self, width=200, placeholder_text="Destination", border_color="grey")
        self.destination_entry.grid(row=2, column=0, padx=30, pady=15)
        self.class_entry = ctk.CTkEntry(self, width=200, placeholder_text="Class", border_color="grey")
        self.class_entry.grid(row=3, column=0, padx=30, pady=15)
        self.time_entry = ctk.CTkEntry(self, width=200, placeholder_text="Time", border_color="grey")
        self.time_entry.grid(row=4, column=0, padx=30, pady=15)
        self.price_entry = ctk.CTkEntry(self, width=200, placeholder_text="Price", border_color="grey")
        self.price_entry.grid(row=5, column=0, padx=30, pady=15)

        self.error_text = tk.StringVar()
        self.error_label = ctk.CTkLabel(self, textvariable=self.error_text, font=ctk.CTkFont(size=15))
        self.error_label.grid(row=6, column=0)

        self.submit_btn = ctk.CTkButton(self, text="Submit", command=self.submit)
        self.submit_btn.grid(row=7, column=0, padx=30, pady=15, sticky="e")
        
    def submit(self):
        details = (
            self.airline_entry.get(),
            self.pod_entry.get(),
            self.destination_entry.get(),
            self.class_entry.get(),
            self.time_entry.get(),
            self.price_entry.get()
        )

        if self.verification(details) is False:
            return

        self.submit_command(details)

    def verification(self, target):
        for i in target:
            if i.strip() == '':
                self.error_text.set("All fields must be filled")
                return False

        try:
            int(target[-1])
        except ValueError:
            self.error_text.set("Price should be a number")
            return False

        return True