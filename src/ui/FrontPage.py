import customtkinter as ctk
from widget.BgFrame import BgFrame

class FrontPage(BgFrame):
    def __init__(self, root):
        super().__init__(root, "login_bg.png", 1, 1)

        self.content_frame = ctk.CTkFrame(self.bg_image_label, fg_color="transparent")
        self.content_frame.grid(row=0, column=0, sticky="ns")

        self.content_frame.grid_rowconfigure(0, weight=1)

        self.container_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.container_frame.grid(row=0, column=0)

        self.heading = ctk.CTkLabel(self.container_frame, text="AirLine", font=ctk.CTkFont(size=30, weight="bold"), fg_color="transparent")
        self.heading.grid(row=0, column=0)

        self.btn_frame = ctk.CTkFrame(self.container_frame, fg_color="transparent")
        self.btn_frame.grid(row=1, column=0, padx=35, pady=30)

        self.login_btn = ctk.CTkButton(self.btn_frame, text="Login", command=self.loginAccount, width=200)
        self.login_btn.grid(row=0, column=0, pady=(0, 10))

        self.signin_btn = ctk.CTkButton(self.btn_frame, text="Sign up", command=self.signinAccount, width=200)
        self.signin_btn.grid(row=1, column=0, pady=(0, 10))

        self.root.initFrame("SignUp")
        self.root.initFrame("Login")

    def loginAccount(self):
        self.root.showFrame("Login")

    def signinAccount(self):
        self.root.showFrame("SignUp")