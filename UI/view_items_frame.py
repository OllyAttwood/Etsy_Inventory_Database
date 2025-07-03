import customtkinter
from tkinter import StringVar
from UI.custom_table import CustomTable
from UI.filter_bar_frame import FilterBarFrame
from UI.adjust_stock_level_popup import AdjustStockLevelPopup

class ViewItemsFrame(customtkinter.CTkFrame):
    def __init__(self, master, presenter, tab_view):
        super().__init__(master)
        self.master = master
        self.presenter = presenter
        self.tab_view = tab_view

        self.init_filter_bar()

        #set up table
        full_data = self.presenter.get_filtered_items() #gets initial data
        self.create_table(full_data["data"], full_data["column_names"])

        self.create_adjust_stock_level_button()

        self.grid_columnconfigure(0, weight=1)

    def update_table(self, filters):
        self.table.grid_forget()
        full_data = self.presenter.get_filtered_items(filters)
        self.create_table(full_data["data"], full_data["column_names"])

    def init_filter_bar(self):
        design_options = self.presenter.get_product_designs()
        theme_options = self.presenter.get_product_themes()
        type_options = self.presenter.get_product_types()
        sub_type_options = self.presenter.get_product_sub_types()
        colour_options =  self.presenter.get_product_colours()

        self.filter_bar = FilterBarFrame(self, design_options, theme_options, type_options, sub_type_options, colour_options)
        self.filter_bar.grid(row=0, column=0, pady=10)

    def create_table(self, data_rows, column_names):
        self.table = CustomTable(self, data_rows, column_names)
        self.table.grid(row=1, column=0)

    def create_adjust_stock_level_button(self):
        self.adjust_stock_level_button = customtkinter.CTkButton(self, text="Adjust stock level...", command=self.on_adjust_stock_level_button_click)
        self.adjust_stock_level_button.grid(row=2, column=0)

    def on_adjust_stock_level_button_click(self):
        selected_item_name, selected_item_id = self.table.get_selected_row_item_name_and_id()
        selected_item_type = self.filter_bar.get_current_filter_values()["Item Type"]

        AdjustStockLevelPopup(selected_item_name, selected_item_id, selected_item_type, self.presenter, self.tab_view)
