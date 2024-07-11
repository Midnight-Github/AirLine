import customtkinter as ctk
from var.Globals import user_manager

class SideBar(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root)

        self.root = root

        self.signout_btn = ctk.CTkButton(self, text="Sign out", command=self.signOut)
        self.signout_btn.grid(row=0, column=0)

    def signOut(self):
        user_manager.data["current"]["name"] = "None"
        user_manager.push()

        self.root.reinitFrameAll()

        self.root.showFrame("FrontPage")