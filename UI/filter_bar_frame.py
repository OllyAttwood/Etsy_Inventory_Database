import customtkinter
from tkinter import StringVar

class FilterBarFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # padding vars
        self.lbl_padx = 10
        self.widget_padx= (0,10)
        self.pady = 10 # pady for both labels and other widgets
        # widget position counter
        self.current_widget_num = 0

        # item type
        product_component_lbl = customtkinter.CTkLabel(self, text="Item Type:")
        self.add_label(product_component_lbl)
        product_component_vals = ["Product", "Component"]
        product_component_switch = customtkinter.CTkSegmentedButton(self, values=product_component_vals)
        product_component_switch.set(product_component_vals[0])
        self.add_input_widget(product_component_switch)

        # name
        name_lbl = customtkinter.CTkLabel(self, text="Name:")
        self.add_label(name_lbl)
        name_entry = customtkinter.CTkEntry(self)
        self.add_input_widget(name_entry)

        # design
        design_lbl = customtkinter.CTkLabel(self, text="Design:")
        self.add_label(design_lbl)
        design_dropdown = customtkinter.CTkOptionMenu(self, values = ["", "Design1", "Design2", "Design3"])
        self.add_input_widget(design_dropdown)

        # design theme
        design_theme_lbl = customtkinter.CTkLabel(self, text="Theme:")
        self.add_label(design_theme_lbl)
        design_theme_dropdown = customtkinter.CTkOptionMenu(self, values = ["", "Theme1", "Theme2", "Theme3"])
        self.add_input_widget(design_theme_dropdown)

        # type
        type_lbl = customtkinter.CTkLabel(self, text="Type:")
        self.add_label(type_lbl)
        type_dropdown = customtkinter.CTkOptionMenu(self, values = ["", "Type1", "Type2", "Type3"])
        self.add_input_widget(type_dropdown)

        # sub-type
        sub_type_lbl = customtkinter.CTkLabel(self, text="Sub-type:")
        self.add_label(sub_type_lbl)
        sub_type_dropdown = customtkinter.CTkOptionMenu(self, values = ["", "Sub-type1", "Sub-type2", "Sub-type3"])
        self.add_input_widget(sub_type_dropdown)

        # colour
        colour_lbl = customtkinter.CTkLabel(self, text="Colour:")
        self.add_label(colour_lbl)
        colour_dropdown = customtkinter.CTkOptionMenu(self, values = ["", "Colour1", "Colour2", "Colour3"])
        self.add_input_widget(colour_dropdown)

    def add_label(self, lbl_widget):
        lbl_widget.grid(row=0, column=self.current_widget_num, padx=self.lbl_padx, pady=self.pady)
        self.current_widget_num += 1

    def add_input_widget(self, widget):
        widget.grid(row=0, column=self.current_widget_num, padx=self.widget_padx, pady=self.pady)
        self.current_widget_num += 1
