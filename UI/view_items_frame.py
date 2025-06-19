import customtkinter
from tkinter import StringVar
from UI.custom_table import CustomTable
from UI.filter_bar_frame import FilterBarFrame

class ViewItemsFrame(customtkinter.CTkFrame):
    def __init__(self, master, presenter):
        super().__init__(master)

        self.presenter = presenter

        filter_bar = FilterBarFrame(self)
        filter_bar.grid(row=0, column=0, pady=10)

        full_data = self.presenter.get_filtered_products() #gets initial data

        self.table = CustomTable(self, full_data["data"], full_data["column_names"])
        self.table.grid(row=1, column=0)

        self.grid_columnconfigure(0, weight=1)

    def update_table(self, data=[]):
        self.table.grid_forget()

        #TODO update table with new filters
