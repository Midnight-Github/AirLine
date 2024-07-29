import customtkinter as ctk

class AddFlight(ctk.CTkToplevel):
    def __init__(self, root):
        super.__init__(root)

        self.root = root

        self.flight_details_frame = ctk.CTkFrame(self)
        self.username_entry = ctk.CTkEntry(self.flight_details_frame, width=200, placeholder_text="username", border_color="grey")
        self.username_entry.grid(row=0, column=0, padx=30, pady=15, columnspan=2)
        self.username_entry = ctk.CTkEntry(self.flight_details_frame, width=200, placeholder_text="username", border_color="grey")
        self.username_entry.grid(row=1, column=0, padx=30, pady=15, columnspan=2)
        self.username_entry = ctk.CTkEntry(self.flight_details_frame, width=200, placeholder_text="username", border_color="grey")
        self.username_entry.grid(row=2, column=0, padx=30, pady=15, columnspan=2)
        self.username_entry = ctk.CTkEntry(self.flight_details_frame, width=200, placeholder_text="username", border_color="grey")
        self.username_entry.grid(row=3, column=0, padx=30, pady=15, columnspan=2)
        self.username_entry = ctk.CTkEntry(self.flight_details_frame, width=200, placeholder_text="username", border_color="grey")
        self.username_entry.grid(row=4, column=0, padx=30, pady=15, columnspan=2)
        self.username_entry = ctk.CTkEntry(self.flight_details_frame, width=200, placeholder_text="username", border_color="grey")
        self.username_entry.grid(row=5, column=0, padx=30, pady=15, columnspan=2)