import customtkinter
from tkinter import StringVar
from UI.custom_table import CustomTable
from UI.filter_bar_frame import FilterBarFrame
from UI.adjust_stock_level_popup import AdjustStockLevelPopup
from UI.messagebox import MessageBox
from UI.small_popup import SmallPopup

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

        self.adjust_stock_level_button = customtkinter.CTkButton(buttons_frame, text="Adjust Stock Level...", command=self.on_adjust_stock_level_button_click)
        self.adjust_stock_level_button.grid(row=0, column=0)

        self.view_components_button = customtkinter.CTkButton(buttons_frame, text="View Product's Components", command=self.on_view_components_button_click)
        self.view_components_button.grid(row=0, column=1)

        self.delete_item_button = customtkinter.CTkButton(buttons_frame, text="Delete Item", command=self.on_delete_button)
        self.delete_item_button.grid(row=0, column=2)

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

    def on_delete_button(self):
        selected_item_name, selected_item_id = self.table.get_selected_row_item_name_and_id()
        selected_item_type = self.filter_bar.get_current_filter_values()["Item Type"]

        ConfirmItemDeletePopup(selected_item_name, selected_item_id, selected_item_type, self.presenter, self.tab_view)


class ViewProductsComponentsPopup(SmallPopup):
    def __init__(self, product_name, component_ids_and_quantities, presenter):
        super().__init__()
        self.title(f"{product_name} Components")
        self.presenter = presenter

        component_ids = [component_data[0] for component_data in component_ids_and_quantities]
        quantities = [component_data[1] for component_data in component_ids_and_quantities]
        component_names = [self.presenter.get_component_name_from_id(component_id)[0] for component_id in component_ids]
        table = CustomTable(self, list(zip(component_names, quantities)), ["Component Name", "Quantity"])
        table.grid(row=0, column=0)

class ConfirmItemDeletePopup(SmallPopup):
    def __init__(self, item_name, item_id, item_type, presenter, tab_view):
        super().__init__()
        self.geometry("350x200")
        self.title(f"Delete {item_type}?")

        self.item_id = item_id
        self.item_type = item_type
        self.presenter = presenter
        self.tab_view = tab_view

        self.grid_columnconfigure(0, weight=1)

        self.text_label = customtkinter.CTkLabel(self, text=f"""Are you sure you want to delete the following {item_type.lower()}:
                                                             \n{item_name}""",
                                                       wraplength=300)
        self.text_label.grid(row=0, column=0)

        # buttons
        button_frame = customtkinter.CTkFrame(self)
        button_frame.grid(row=1, column=0)

        yes_button = customtkinter.CTkButton(button_frame, text="Yes", command=self.on_yes_button_click)
        yes_button.grid(row=0, column=0)

        no_button = customtkinter.CTkButton(button_frame, text="No", command=self.on_no_button_click)
        no_button.grid(row=0, column=1)

    def on_yes_button_click(self):
        if self.item_type == "Product":
            self.presenter.delete_product(self.item_id)
            self.tab_view.reload_all_frames()
            self.release_focus_and_hide()
        elif self.item_type == "Component":
            self.presenter.delete_component(self.item_id)
            self.tab_view.reload_all_frames(display_components_in_view_items_frame=True)
            self.release_focus_and_hide()

    def on_no_button_click(self):
        self.release_focus_and_hide()
