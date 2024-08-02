import customtkinter as ctk
from os import path
from PIL import Image
from reader.Logger import Logger

class BgFrame(ctk.CTkFrame):
    def __init__(self, root, img_name, height_factor, width_factor):
        super().__init__(root, fg_color="transparent")

        self.root = root
        self.height_factor = height_factor
        self.width_factor = width_factor

        self.bind("<Configure>", self.resizeBgImg)

        self.bg_img_path = path.dirname(__file__) + f"\\..\\data\\assets\\{img_name}"

        self.setBgSize()

        self.bg_image_label = ctk.CTkLabel(self, image=self.bg_img, text='')
        self.bg_image_label.grid(row=0, column=0, sticky='nesw')

    def setBgSize(self):
        height = self.winfo_height()
        width = self.winfo_width()

        if height > 1 and width > 1:
            height *= self.height_factor
            width *= self.width_factor

        self.bg_img = ctk.CTkImage(dark_image=Image.open(self.bg_img_path), light_image=Image.open(self.bg_img_path), size=(width, height))

    def resizeBgImg(self, e):
        self.setBgSize()
        self.bg_image_label.configure(image=self.bg_img)

