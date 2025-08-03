import customtkinter
from UI.custom_table import CustomTable
from UI import config

class LowStockFrame(customtkinter.CTkFrame):
    """A frame which displays the items which have a stock level less than or equal to their stock warning value"""

    def __init__(self, master, presenter):
        super().__init__(master)
        self.presenter = presenter

        # product table
        low_stock_product_data = self.presenter.get_low_stock_items(products=True, components=False)
        self.add_table("Low Stock Products", 0, low_stock_product_data)

        #component table
        low_stock_component_data = self.presenter.get_low_stock_items(products=False, components=True)
        self.add_table("Low Stock Components", 2, low_stock_component_data)

        self.grid_columnconfigure(0, weight=1) #puts everything in the middle

    def create_label(self, text, font_size=25):
        """Creates labels with the same appearance"""
        return customtkinter.CTkLabel(self, text=text, font=(None, font_size))

    def add_table(self, title, starting_row_index, item_data, space_between_tables=50):
        """Adds a table to the frame at the given starting row"""
        title_label = self.create_label(title)
        title_label.grid(row=starting_row_index, column=0, pady=config.WIDGET_Y_PADDING)
        table = CustomTable(self, item_data["data"], item_data["column_names"])
        table.grid(row=starting_row_index+1, column=0, sticky="nsew", pady=(0, space_between_tables)) #the pady is to create a gap between the different tables
