import customtkinter as ctk

class Login(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root, fg_color="red")

        self.root = root

        # self.home_btn = ctk.CTkButton(self, text="Home", command=lambda : root.showFrame("Home"))
        # self.home_btn.pack()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # load and create background image
        # current_path = os.path.dirname(os.path.realpath(__file__))
        # self.bg_image = ctk.CTkImage(Image.open(current_path + "/Image.png"),
        #                                         size=(self.width, self.height))
        # self.bg_image_label = ctk.CTkLabel(self, image=self.bg_image)
        # self.bg_image_label.grid(row=0, column=0)

        # create login frame
        self.login_frame = ctk.CTkFrame(self, corner_radius=0)
        self.login_frame.grid(row=0, column=0, sticky="ns")
        self.login_label = ctk.CTkLabel(self.login_frame, text="CustomTkinter\nLogin Page",
                                                    font=ctk.CTkFont(size=20, weight="bold"))
        self.login_label.grid(row=0, column=0, padx=30, pady=(150, 15))
        self.username_entry = ctk.CTkEntry(self.login_frame, width=200, placeholder_text="username")
        self.username_entry.grid(row=1, column=0, padx=30, pady=(15, 15))
        self.password_entry = ctk.CTkEntry(self.login_frame, width=200, show="*", placeholder_text="password")
        self.password_entry.grid(row=2, column=0, padx=30, pady=(0, 15))
        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.login_event, width=200)
        self.login_button.grid(row=3, column=0, padx=30, pady=(15, 15))

    def login_event(self):
        print("Login pressed - username:", self.username_entry.get(), "password:", self.password_entry.get())

        self.login_frame.grid_forget()
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=100)

    def back_event(self):
        self.back