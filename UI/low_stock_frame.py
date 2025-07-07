import customtkinter
from UI.custom_table import CustomTable
from UI import config

class LowStockFrame(customtkinter.CTkFrame):
    def __init__(self, master, presenter):
        super().__init__(master)
        self.presenter = presenter
        space_between_tables = 50

        # product table
        products_label = self.create_label("Low Stock Products")
        products_label.grid(row=0, column=0, pady=config.WIDGET_Y_PADDING)
        low_stock_product_data = self.presenter.get_low_stock_items(products=True, components=False)
        product_table = CustomTable(self, low_stock_product_data["data"], low_stock_product_data["column_names"])
        product_table.grid(row=1, column=0, sticky="nsew", pady=(0, space_between_tables)) #the pady is to create a gap between the products and components

        #component table
        components_label = self.create_label("Low Stock Components")
        components_label.grid(row=2, column=0, pady=config.WIDGET_Y_PADDING)
        low_stock_component_data = self.presenter.get_low_stock_items(products=False, components=True)
        component_table = CustomTable(self, low_stock_component_data["data"], low_stock_component_data["column_names"])
        component_table.grid(row=3, column=0, sticky="nsew",)

        self.grid_columnconfigure(0, weight=1) #puts everything in the middle

    def create_label(self, text, font_size=25):
        return customtkinter.CTkLabel(self, text=text, font=(None, font_size))
