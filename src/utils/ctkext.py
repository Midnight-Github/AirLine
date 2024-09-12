import customtkinter as ctk

def labeledComboBox(master, text, width, values, row, column, padx=0, pady=0, state="readonly"):
    container_frame = ctk.CTkFrame(master, fg_color="transparent")
    container_frame.grid(row=row, column=column, padx=padx, pady=pady, sticky="nesw")
    label = ctk.CTkLabel(container_frame, text=text)
    label.grid(row=0, column=0, sticky="w", padx=10)
    combo_box = ctk.CTkComboBox(container_frame, state=state, border_color="grey", values=values, width=width)
    combo_box.grid(row=1, column=0, sticky="nesw")
    return combo_box