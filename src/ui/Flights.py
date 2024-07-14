import customtkinter as ctk

class Flights(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root)

        self.root = root
        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=1)

        self.header_frame=ctk.CTkFrame(self,fg_color='transparent')
        self.header_frame.grid(row=0, column=0, sticky='nesw')
        self.airline_label=ctk.CTkLabel(self.header_frame, text='Airline', font=ctk.CTkFont(size=15, weight="bold"))
        self.airline_label.grid(row=0, column=0, padx=15)
        self.pod_label=ctk.CTkLabel(self.header_frame, text='Place Of Departure', font=ctk.CTkFont(size=15, weight="bold"))
        self.pod_label.grid(row=0, column=1, padx=15)
        self.dest_label=ctk.CTkLabel(self.header_frame, text='Destination', font=ctk.CTkFont(size=15, weight="bold"))
        self.dest_label.grid(row=0, column=2, padx=15)
        self.class_label=ctk.CTkLabel(self.header_frame, text='Class', font=ctk.CTkFont(size=15, weight="bold"))
        self.class_label.grid(row=0, column=3, padx=15)
        self.tod_label=ctk.CTkLabel(self.header_frame, text='Time Of Departure', font=ctk.CTkFont(size=15, weight="bold"))
        self.tod_label.grid(row=0, column=4, padx=15)
        self.duration_label=ctk.CTkLabel(self.header_frame, text='Duration', font=ctk.CTkFont(size=15, weight="bold"))
        self.duration_label.grid(row=0, column=5, padx=15)
        self.price_label=ctk.CTkLabel(self.header_frame, text='Price', font=ctk.CTkFont(size=15, weight="bold"))
        self.price_label.grid(row=0, column=6, padx=15)

        self.flights_frame=ctk.CTkFrame(self,fg_color='red')
        self.flights_frame.grid(row=1, column=0, sticky='nesw')

        self.button_frame=ctk.CTkFrame(self,fg_color='transparent')
        self.button_frame.grid(row=2, column=0, sticky='sew')

        self.back_btn = ctk.CTkButton(self.button_frame, text="back", command=lambda : self.root.showFrame("Home"))
        self.back_btn.grid(row=0, column=0)
        self.addflight_btn = ctk.CTkButton(self.button_frame, text="Add a Flight")
        self.addflight_btn.grid(row=0, column=1)
