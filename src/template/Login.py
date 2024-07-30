import customtkinter as ctk
from os import path
from PIL import Image

class Login(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root, fg_color="transparent")

        self.root = root

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.bind("<Configure>", self.resizeBgImg)

        self.bg_img_path = path.dirname(__file__) + "\\..\\data\\assets\\login_bg_img.png"

        self.setBgSize()

        self.bg_image_label = ctk.CTkLabel(self, image=self.bg_img, text='')
        self.bg_image_label.grid(row=0, column=0, sticky="nesw")

        self.content_frame = ctk.CTkFrame(self.bg_image_label, fg_color="transparent")
        self.content_frame.grid(row=0, column=0, sticky="ns")

    def setBgSize(self):
        height = self.winfo_height()
        width = self.winfo_width()
        self.bg_img = ctk.CTkImage(dark_image=Image.open(self.bg_img_path), light_image=Image.open(self.bg_img_path), size=(width, height))

    def resizeBgImg(self, e):
        self.setBgSize()
        self.bg_image_label.configure(image=self.bg_img)

