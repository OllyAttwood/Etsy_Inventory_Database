import customtkinter
from tkinter import StringVar
from custom_table import CustomTable

class ViewItemsFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        test_data = [["necklace", 1, 3],
                     ["earrings", 2, 1],
                     ["bauble", 3, 2]]
        test_cols = ["Item", "ID", "Stock"]
        self.table = CustomTable(self, test_data, test_cols)
        self.table.grid(row=0, column=0)
