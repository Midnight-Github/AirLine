import customtkinter as ctk

class Home(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root)

        self.root = root

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=0, sticky="nesw")

        self.page1_btn = ctk.CTkButton(self.content_frame, text="Page1", command=lambda : root.showFrame("Page1"))
        self.page1_btn.grid(row=0, column=0)
        self.page2_btn = ctk.CTkButton(self.content_frame, text="Page2", command=lambda : root.showFrame("Page2"))
        self.page2_btn.grid(row=0, column=1)