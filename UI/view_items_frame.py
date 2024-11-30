import customtkinter

class ViewItemsFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        lbl = customtkinter.CTkLabel(self, text="View Items!", font=(None, 100))
        lbl.grid(row=0, column=0)
