import customtkinter

class AddNewItemFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        lbl = customtkinter.CTkLabel(self, text="Add New Item!", font=(None, 100))
        lbl.grid(row=0, column=0)
