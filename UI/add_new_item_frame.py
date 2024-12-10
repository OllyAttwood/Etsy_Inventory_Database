import customtkinter
from spinbox import Spinbox

class AddNewItemFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.widget_grid = []

        # item type
        product_component_lbl_str = "Item Type:"
        product_component_vals = ["Product", "Component"]
        product_component_switch = customtkinter.CTkSegmentedButton(self, values=product_component_vals)
        product_component_switch.set(product_component_vals[0])
        self.widget_grid.append([product_component_lbl_str, product_component_switch])

        # name
        name_lbl_str = "Name:"
        name_entry = customtkinter.CTkEntry(self)
        self.widget_grid.append([name_lbl_str, name_entry])

        # theme
        theme_lbl_str = "Theme:"
        theme_dropdown = customtkinter.CTkOptionMenu(self, values = ["", "Theme1", "Theme2", "Theme3"])
        new_theme_button = customtkinter.CTkButton(self, text="Add new theme... ")
        self.widget_grid.append([theme_lbl_str, theme_dropdown, new_theme_button])

        # design
        design_lbl_str = "Design:"
        design_dropdown = customtkinter.CTkOptionMenu(self, values = ["", "Design1", "Design2", "Design3"])
        new_design_button = customtkinter.CTkButton(self, text="Add new design... ")
        self.widget_grid.append([design_lbl_str, design_dropdown, new_design_button])

        # colour
        colour_lbl_str = "Colour:"
        colour_dropdown = customtkinter.CTkOptionMenu(self, values = ["", "colour1", "colour2", "colour3"])
        new_colour_button = customtkinter.CTkButton(self, text="Add new colour... ")
        self.widget_grid.append([colour_lbl_str, colour_dropdown, new_colour_button])

        # type
        type_lbl_str = "Type:"
        type_dropdown = customtkinter.CTkOptionMenu(self, values = ["", "type1", "type2", "type3"])
        new_type_button = customtkinter.CTkButton(self, text="Add new type... ")
        self.widget_grid.append([type_lbl_str, type_dropdown, new_type_button])

        # subtype
        subtype_lbl_str = "Sub-Type:"
        subtype_dropdown = customtkinter.CTkOptionMenu(self, values = ["", "subtype1", "subtype2", "subtype3"])
        new_subtype_button = customtkinter.CTkButton(self, text="Add new subtype... ")
        self.widget_grid.append([subtype_lbl_str, subtype_dropdown, new_subtype_button])

        # stock
        stock_lbl_str = "Stock:"
        stock_spinbox = Spinbox(self)
        self.widget_grid.append([stock_lbl_str, stock_spinbox])

        # low stock
        low_stock_lbl_str = "Low Stock Warning:"
        low_stock_spinbox = Spinbox(self)
        self.widget_grid.append([low_stock_lbl_str, low_stock_spinbox])

        #loop through widget_grid, adding widgets
        for row_num, row_widgets in enumerate(self.widget_grid):
            for col_num, widget in enumerate(row_widgets):
                #create label widget from label strings
                if col_num == 0:
                    widget = customtkinter.CTkLabel(self, text=widget)

                widget.grid(row=row_num, column=col_num)
