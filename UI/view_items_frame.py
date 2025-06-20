import customtkinter
from tkinter import StringVar
from UI.custom_table import CustomTable
from UI.filter_bar_frame import FilterBarFrame

class ViewItemsFrame(customtkinter.CTkFrame):
    def __init__(self, master, presenter):
        super().__init__(master)

        self.presenter = presenter

        self.init_filter_bar()

        #set up table
        full_data = self.presenter.get_filtered_products() #gets initial data
        self.table = CustomTable(self, full_data["data"], full_data["column_names"])
        self.table.grid(row=1, column=0)

        self.grid_columnconfigure(0, weight=1)

    def update_table(self, data=[]):
        self.table.grid_forget()

        #TODO update table with new filters

    def init_filter_bar(self):
        design_options = self.presenter.get_product_designs()
        theme_options = self.presenter.get_product_themes()
        type_options = self.presenter.get_product_types()
        sub_type_options = self.presenter.get_product_sub_types()
        colour_options =  self.presenter.get_product_colours()

        self.filter_bar = FilterBarFrame(self, design_options, theme_options, type_options, sub_type_options, colour_options)
        self.filter_bar.grid(row=0, column=0, pady=10)
