import customtkinter as ctk
from var.ConfigManager import server_config
from reader.Logger import Logger
from var.SqlManager import mysql
from ui.AddFlightForm import AddFlightForm
from var.Globals import get_user_role
from CTkMessagebox import CTkMessagebox as ctkmsgbox
from datetime import datetime
from widget.TreeView import TreeView
from ui.ShowPassengers import ShowPassengers

logger = Logger(__name__).logger

class Flights(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1,weight=1)

        self.root = root

        self.heading_label = ctk.CTkLabel(self, text="Flights", font=ctk.CTkFont(size=30, weight="bold"))
        self.heading_label.grid(row=0, column=0, columnspan=2, pady=5)

        self.tree_view = TreeView(self, columns=('ID', 'Airline', 'Place of Departure', 'Destination', 'Class', 'Date', 'Time', 'Price'))
        self.tree_view.grid(row=1, column=1, rowspan=3, sticky="nesw")

        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.grid(row=1, column=0, sticky='n', padx=10)

        self.refresh_btn = ctk.CTkButton(self.btn_frame, text="Refresh", command=self.refresh)
        self.refresh_btn.grid(row=0, column=0, padx=10, pady=(10, 20))      
        self.book_btn = ctk.CTkButton(self.btn_frame, text="Book Flight", command=self.BookFlight)
        self.book_btn.grid(row=1, column=0, padx=10, pady=(0, 20))    
        self.back_btn = ctk.CTkButton(self.btn_frame, text="Back", command=lambda : self.root.showFrame("Home"))
        self.back_btn.grid(row=6, column=0, padx=10, pady=(0, 10))
        
        if server_config.data["user"]["permission"] > 0:
            self.adminFeatures()

        self.refresh()

    def adminFeatures(self):
        self.add_flight_form_toplevel = None
        self.show_passengers_toplevel = None

        self.add_btn = ctk.CTkButton(self.btn_frame, text="Add Flight", command=self.launchFlightForm)
        self.add_btn.grid(row=2, column=0, padx=10, pady=(0, 20))

        self.delete_btn = ctk.CTkButton(self.btn_frame, text="Delete Flight", command=self.deleteFlight)
        self.delete_btn.grid(row=3, column=0, padx=10, pady=(0, 20))
        
        self.show_passengers_btn = ctk.CTkButton(self.btn_frame, text="Show Passengers", command=self.launchShowPassengers)
        self.show_passengers_btn.grid(row=4, column=0, padx=10, pady=(0, 20))

        self.rb_frame = ctk.CTkFrame(self)
        self.rb_frame.grid(row=3, column=0, pady=10, ipadx=15)

        self.rb_label = ctk.CTkLabel(self.rb_frame, text = "Search By", font=ctk.CTkFont(size=20, weight="bold"))
        self.rb_label.grid(row=1, column=0, pady=10)
        
        self.radio_var = ctk.StringVar(value="select_flights_by_radio_btn")
        self.all_flights_rb = ctk.CTkRadioButton(self.rb_frame, text="All Flights", radiobutton_height=15, radiobutton_width=15, border_width_checked=5, variable=self.radio_var, command=lambda : self.updateRadioBtn("all"))
        self.all_flights_rb.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.available_flights_rb = ctk.CTkRadioButton(self.rb_frame, text="Available Flights", radiobutton_height=15, radiobutton_width=15, border_width_checked=5, variable=self.radio_var, command=lambda : self.updateRadioBtn("available"))
        self.available_flights_rb.grid(row=3, column=0, padx=10, pady=10, sticky='w')
        self.expired_flights_rb = ctk.CTkRadioButton(self.rb_frame, text="Expired Flights", radiobutton_height=15, radiobutton_width=15, border_width_checked=5, variable=self.radio_var, command=lambda : self.updateRadioBtn("expired"))
        self.expired_flights_rb.grid(row=4, column=0, padx=10, pady=10, sticky='w')

        match(server_config.data["user"]["show_flights_by"]):
            case "all":
                self.all_flights_rb.select()
            case "available":
                self.available_flights_rb.select()
            case "expired":
                self.expired_flights_rb.select()

    def refresh(self):
        logger.info("Refreshing Flights!")
        self.tree_view.reloadTable(self.getRowsFlights())

    # main functions:
    def addFlight(self, row):
        self.insertRowFlights(row)

        self.refresh()

        if self.isAddFlightFormAlive():
            self.add_flight_form_toplevel.destroy() # pyright: ignore

    def deleteFlight(self):
        selected = self.tree_view.getSelectedRow()
        if selected is None:
            ctkmsgbox(title="Delete flight", message="No flight selected!")
            return
        msg = ctkmsgbox(title="Delete flight", message="Are you sure you want to delete this flight?", icon="question", option_1="Yes", option_2="No")
        if msg.get() != "Yes":
            return

        self.deleteRowFlights(selected[0]) # passing flight id

        self.refresh()

        ctkmsgbox(title="Delete flight", message="Successfully deleted this flight!", icon="check")

        self.root.reinitFrame("Cart")
        self.root.showFrame("Flights")

    def BookFlight(self):
        selected = self.tree_view.getSelectedRow()
        if selected is None:
            ctkmsgbox(title="Book flight", message="No flight selected!")
            return

        msg = ctkmsgbox(title="Book flight", message="Are you sure you want to Book this flight", icon="question", option_1="Yes", option_2="No")
        if msg.get() != "Yes":
            return

        flight_id = selected[0]
        date, time = str(datetime.now()).split()
        result = mysql.execute(f"SELECT * FROM Flights WHERE Flight_ID = {flight_id} AND (Date > DATE('{date}') OR (Date = DATE('{date}') AND Time >= TIME('{time}')));", buffered=True)
        if result[0] is False:
            logger.error(f"Failed to extract flight with id: {flight_id} from Flights!")
            logger.error(result[1])
            return
        if not result[1]:
            ctkmsgbox(title="Book flight", message="You cannot book expired flight!", icon="warning")
            logger.warning(f"{get_user_role[server_config.data["user"]["permission"]]}: {server_config.data["user"]["name"]} tried to book expired flight with id: {flight_id}")
            return

        result = mysql.execute(f"INSERT INTO Passengers VALUES('{server_config.data["user"]["name"]}', {flight_id});")
        
        if result[0] is False:
            if "Duplicate entry" in str(result[1]):
                ctkmsgbox(title="Book flight", message="You have already booked this flight")
                logger.warning(f"{get_user_role[server_config.data["user"]["permission"]]}: {server_config.data["user"]["name"]} tried to rebook flight with id: {flight_id}")
                return
            logger.error("Failed to insert data to Passengers!")
            logger.error(result[1])
            return
        
        ctkmsgbox(title="Book flight", message="Successfully booked flight!",icon="check")
        logger.info(f"{get_user_role[server_config.data["user"]["permission"]]}: {server_config.data["user"]["name"]} booked Flight with id: {flight_id}")
        self.root.reinitFrame("Cart")
        self.root.showFrame("Flights")

    # add flight form functions:
    def isAddFlightFormAlive(self):
        return not (self.add_flight_form_toplevel is None or not self.add_flight_form_toplevel.winfo_exists())

    def launchFlightForm(self):
        if not self.isAddFlightFormAlive():
            self.add_flight_form_toplevel = AddFlightForm(self.addFlight)
        
        self.add_flight_form_toplevel.after(100, self.add_flight_form_toplevel.lift) #pyright: ignore # work around to fix bug: toplevel hiding behind root
        
    # show passengers functions:
    def launchShowPassengers(self):
        selected = self.tree_view.getSelectedRow()
        if selected is None:
            ctkmsgbox(title="Passengers", message="No flights selected")
            return
        
        if self.isShowPassengersAlive():
            self.show_passengers_toplevel.destroy() # pyright: ignore
        
        flight_id = selected[0]
        self.show_passengers_toplevel = ShowPassengers(flight_id)
        self.show_passengers_toplevel.after(100, self.show_passengers_toplevel.lift) #pyright: ignore # work around to fix bug: toplevel hiding behind root
        
    def isShowPassengersAlive(self):
        return not (self.show_passengers_toplevel is None or not self.show_passengers_toplevel.winfo_exists())

    # database functions:
    def getRowsFlights(self):
        date, time = str(datetime.now()).split()

        if server_config.data["user"]["permission"] == 0:
            return self.getAvailableFlights(date, time)
            
        match(server_config.data["user"]["show_flights_by"]):
            case "all":
                rows = self.getAllFlights()
            case "available":
                rows = self.getAvailableFlights(date, time)
            case "expired":
                rows = self.getExpiredFlights(date, time)
            case _:
                logger.error(f"Incorrect server_config.data[\"User\"][\"show_flights_by\"] value: {server_config.data["User"]["show_flights_by"]}")
                return

        return rows

    def insertRowFlights(self, row):
        sql_cmd = f"INSERT INTO Flights {str(tuple(row.keys())).replace('\'', '')} VALUES {str(tuple(row.values()))};"
        result = mysql.execute(sql_cmd)

        if result[0] is False:
            logger.error("Failed to insert data to Flights!")
            logger.error(result[1])
            return

        logger.info(f"{get_user_role[server_config.data["user"]["permission"]]}: {server_config.data["user"]["name"]} inserted flight: {row}")
        ctkmsgbox(title="Add flight", message="Successfully added this flight!", icon="check")

    def deleteRowFlights(self, flight_id):
        sql_cmd_del_passengers = f"DELETE FROM Passengers WHERE Flight_ID = {flight_id}"
        sql_cmd_del_flights = f"DELETE FROM Flights WHERE Flight_ID = {flight_id};"
        result_passengers = mysql.execute(sql_cmd_del_passengers)
        result_flights = mysql.execute(sql_cmd_del_flights)

        if result_passengers[0] is False:
            logger.error("Failed to delete data from Passengers!")
            logger.error(result_passengers[1])
            return 
        
        if result_flights[0] is False:
            logger.error("Failed to delete data from Flights!")
            logger.error(result_flights[1])
            return

        logger.info(f"{get_user_role[server_config.data["user"]["permission"]]}: {server_config.data["user"]["name"]} deleted flight with id {flight_id}")
    
    #Sub database functions:
    def getAvailableFlights(self, date, time):
        sql_cmd = f"SELECT * FROM Flights WHERE (Date > DATE('{date}') OR (Date = DATE('{date}') AND Time >= TIME('{time}')));"
        result = mysql.execute(sql_cmd, buffered=True)

        if result[0] is False:
            logger.error("Failed to extract available flights from Flights!")
            logger.error(result[1])
            return
        
        logger.info("Extracted available flights from flights")
        return result[1]
    
    def getExpiredFlights(self, date, time):
        sql_cmd = f"SELECT * FROM Flights WHERE (Date < DATE('{date}') OR (Date = DATE('{date}') AND Time <= TIME('{time}')));"
        result = mysql.execute(sql_cmd, buffered=True)

        if result[0] is False:
            logger.error("Failed to extract expired flights from Flights!")
            logger.error(result[1])
            return
        
        logger.info("Extracted expired flights from Flights!")
        return result[1]
    
    def getAllFlights(self):
        sql_cmd = f"SELECT * FROM Flights;"
        result = mysql.execute(sql_cmd, buffered=True)

        if result[0] is False:
            logger.error("Failed to extract flights from Flights!")
            logger.error(result[1])
            return
        
        logger.info("Extracted flights from Flights!")
        return result[1]

    # radio button functions:
    def updateRadioBtn(self, value):
        server_config.data["user"]["show_flights_by"] = value
        server_config.push()
        self.refresh()
