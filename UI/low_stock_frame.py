import customtkinter

class LowStockFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        lbl = customtkinter.CTkLabel(self, text="Low Stock!", font=(None, 100))
        lbl.grid(row=0, column=0)
