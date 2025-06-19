import customtkinter
from tkinter import StringVar
from custom_table import CustomTable
from filter_bar_frame import FilterBarFrame

class ViewItemsFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        filter_bar = FilterBarFrame(self)
        filter_bar.grid(row=0, column=0, pady=10)

        test_data = [["necklace", 1, 3],
                     ["earrings", 2, 1],
                     ["bauble", 3, 2]]
        test_cols = ["Item", "ID", "Stock"]
        self.table = CustomTable(self, test_data, test_cols)
        self.table.grid(row=1, column=0)

        self.grid_columnconfigure(0, weight=1)

    def update_table(self, data=[]):
        self.table.grid_forget()

        #TODO update table with new filters
