import customtkinter as ctk
from template.Login import Login as login_template

class Home(login_template):
    def __init__(self, root):
        super().__init__(root)

        self.content_frame.grid_rowconfigure(0, weight=1)

        self.container_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.container_frame.grid(row=0, column=0)

        self.heading = ctk.CTkLabel(self.container_frame, text="AirLine", font=ctk.CTkFont(size=30), fg_color="transparent")
        self.heading.grid(row=0, column=0)

        self.btn_frame = ctk.CTkFrame(self.container_frame, fg_color="transparent")
        self.btn_frame.grid(row=1, column=0, padx=50, pady=30)

        self.login_btn = ctk.CTkButton(self.btn_frame, text="Login")
        self.login_btn.grid(row=0, column=0, pady=(0, 10))

        self.create_account_btn = ctk.CTkButton(self.btn_frame, text="Sign in")
        self.create_account_btn.grid(row=1, column=0, pady=(0, 10))