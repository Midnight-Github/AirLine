import customtkinter as ctk
from template.Login import Login as login_template

class Login(login_template):
    def __init__(self, root):
        super().__init__(root)

        self.root = root

        self.content_frame.grid_rowconfigure(0, weight=1)

        self.container_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.container_frame.grid(row=0, column=0)

        # create login frame
        self.login_frame = ctk.CTkFrame(self.container_frame, corner_radius=0, fg_color="transparent")
        self.login_frame.grid(row=0, column=0, sticky="ns")
        self.login_label = ctk.CTkLabel(self.login_frame, text="Login",
                                                    font=ctk.CTkFont(size=30, weight="bold"))
        self.login_label.grid(row=0, column=0, padx=30, pady=(0, 15), columnspan=2)
        self.username_entry = ctk.CTkEntry(self.login_frame, width=200, placeholder_text="username")
        self.username_entry.grid(row=1, column=0, padx=30, pady=15, columnspan=2)
        self.password_entry = ctk.CTkEntry(self.login_frame, width=200, show="*", placeholder_text="password")
        self.password_entry.grid(row=2, column=0, padx=30, pady=(0, 15), columnspan=2)
        self.login_btn = ctk.CTkButton(self.login_frame, text="Login", command=self.loginEvent, width=100)
        self.login_btn.grid(row=3, column=1, padx=(10, 30), pady=15)
        self.back_btn = ctk.CTkButton(self.login_frame, text="Back", command=self.backEvent, width=100)
        self.back_btn.grid(row=3, column=0, padx=(30, 0), pady=15)

    def loginEvent(self):
        print("Login pressed - username:", self.username_entry.get(), "password:", self.password_entry.get())

    def backEvent(self):
        self.root.showFrame("Home")