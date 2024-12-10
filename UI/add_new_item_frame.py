import customtkinter
from spinbox import Spinbox

class AddNewItemFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # item type
        product_component_lbl = customtkinter.CTkLabel(self, text="Item Type:")
        self.add_label(product_component_lbl, row=0)
        product_component_vals = ["Product", "Component"]
        product_component_switch = customtkinter.CTkSegmentedButton(self, values=product_component_vals)
        product_component_switch.set(product_component_vals[0])
        self.add_input_widget(product_component_switch, row=0)

        # name
        name_lbl = customtkinter.CTkLabel(self, text="Name:")
        self.add_label(name_lbl, row=1)
        name_entry = customtkinter.CTkEntry(self)
        self.add_input_widget(name_entry, row=1)

        # theme
        theme_lbl = customtkinter.CTkLabel(self, text="Theme:")
        self.add_label(theme_lbl, row=2)
        theme_dropdown = customtkinter.CTkOptionMenu(self, values = ["", "Theme1", "Theme2", "Theme3"])
        self.add_input_widget(theme_dropdown, row=2)
        new_theme_button = customtkinter.CTkButton(self, text="Add new theme... ")
        self.add_label(new_theme_button, row=2, col=2)

        # design
        design_lbl = customtkinter.CTkLabel(self, text="Design:")
        self.add_label(design_lbl, row=3)
        design_dropdown = customtkinter.CTkOptionMenu(self, values = ["", "Design1", "Design2", "Design3"])
        self.add_input_widget(design_dropdown, row=3)
        new_design_button = customtkinter.CTkButton(self, text="Add new design... ")
        self.add_label(new_design_button, row=3, col=2)

        # colour
        colour_lbl = customtkinter.CTkLabel(self, text="Colour:")
        self.add_label(colour_lbl, row=4)
        colour_dropdown = customtkinter.CTkOptionMenu(self, values = ["", "colour1", "colour2", "colour3"])
        self.add_input_widget(colour_dropdown, row=4)
        new_colour_button = customtkinter.CTkButton(self, text="Add new colour... ")
        self.add_label(new_colour_button, row=4, col=2)

        # type
        type_lbl = customtkinter.CTkLabel(self, text="Type:")
        self.add_label(type_lbl, row=5)
        type_dropdown = customtkinter.CTkOptionMenu(self, values = ["", "type1", "type2", "type3"])
        self.add_input_widget(type_dropdown, row=5)
        new_type_button = customtkinter.CTkButton(self, text="Add new type... ")
        self.add_label(new_type_button, row=5, col=2)

        # subtype
        subtype_lbl = customtkinter.CTkLabel(self, text="Sub-Type:")
        self.add_label(subtype_lbl, row=6)
        subtype_dropdown = customtkinter.CTkOptionMenu(self, values = ["", "subtype1", "subtype2", "subtype3"])
        self.add_input_widget(subtype_dropdown, row=6)
        new_subtype_button = customtkinter.CTkButton(self, text="Add new subtype... ")
        self.add_label(new_subtype_button, row=6, col=2)

        # stock
        stock_lbl = customtkinter.CTkLabel(self, text="Stock:")
        self.add_label(stock_lbl, row=7)
        stock_spinbox = Spinbox(self)
        self.add_input_widget(stock_spinbox, row=7)

        # low stock
        low_stock_lbl = customtkinter.CTkLabel(self, text="Low Stock Warning:")
        self.add_label(low_stock_lbl, row=8)
        low_stock_spinbox = Spinbox(self)
        self.add_input_widget(low_stock_spinbox, row=8)

    def add_label(self, lbl_widget, row, col=0):
        lbl_widget.grid(row=row, column=col)

    def add_input_widget(self, widget, row, col=1):
        widget.grid(row=row, column=col)

    def create_plus_minus_button(self, char):
        return customtkinter.CTkButton(self, text=char, width=self.plus_minus_button_width)
