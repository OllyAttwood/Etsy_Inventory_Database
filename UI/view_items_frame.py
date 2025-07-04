import customtkinter
from tkinter import StringVar
from UI.custom_table import CustomTable
from UI.filter_bar_frame import FilterBarFrame
from UI.adjust_stock_level_popup import AdjustStockLevelPopup
from UI.messagebox import MessageBox

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

        self.create_buttons()

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

    def create_buttons(self):
        buttons_frame = customtkinter.CTkFrame(self)
        buttons_frame.grid(row=2, column=0)

        self.adjust_stock_level_button = customtkinter.CTkButton(buttons_frame, text="Adjust stock level...", command=self.on_adjust_stock_level_button_click)
        self.adjust_stock_level_button.grid(row=0, column=0)

        self.view_components_button = customtkinter.CTkButton(buttons_frame, text="View product's components", command=self.on_view_components_button_click)
        self.view_components_button.grid(row=0, column=1)

    def on_adjust_stock_level_button_click(self):
        selected_item_name, selected_item_id = self.table.get_selected_row_item_name_and_id()
        selected_item_type = self.filter_bar.get_current_filter_values()["Item Type"]

        AdjustStockLevelPopup(selected_item_name, selected_item_id, selected_item_type, self.presenter, self.tab_view)

    def on_view_components_button_click(self):
        selected_item_type = self.filter_bar.get_current_filter_values()["Item Type"]

        if selected_item_type == "Product":
            selected_product_name, selected_product_id = self.table.get_selected_row_item_name_and_id()
            component_ids_and_quantities = self.presenter.get_components_of_product(selected_product_id)

            ViewProductsComponentsPopup(selected_product_name, component_ids_and_quantities, self.presenter)
        else:
            MessageBox("Incorrect Item Type", "You must select a product (not a component) to be able to view its components!")


class ViewProductsComponentsPopup(customtkinter.CTkToplevel):
    def __init__(self, product_name, component_ids_and_quantities, presenter):
        super().__init__()
        self.title(f"{product_name} Components")
        self.presenter = presenter

        # lock popup at front
        self.attributes("-topmost", "true")
        # make main window unclickable until popup is closed
        self.lock_at_front()

        # override the exit button as exiting produces an error, so we just
        # hide the window and restore it if necessary
        self.protocol("WM_DELETE_WINDOW", self.release_focus_and_hide)

        component_ids = [component_data[0] for component_data in component_ids_and_quantities]
        quantities = [component_data[1] for component_data in component_ids_and_quantities]
        component_names = [self.presenter.get_component_name_from_id(component_id)[0] for component_id in component_ids]
        table = CustomTable(self, list(zip(component_names, quantities)), ["Component Name", "Quantity"])
        table.grid(row=0, column=0)

    # hides window
    def release_focus_and_hide(self):
        self.grab_release()
        self.withdraw()

    # make main window unclickable until popup is closed
    def lock_at_front(self):
        self.wait_visibility() # https://raspberrypi.stackexchange.com/a/105522
        self.grab_set()
