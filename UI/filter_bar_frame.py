import customtkinter
from tkinter import StringVar

class FilterBarFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

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
        self.product_component_switch = customtkinter.CTkSegmentedButton(self, values=product_component_vals)
        self.product_component_switch.set(product_component_vals[0])
        self.add_input_widget(self.product_component_switch)

        # name
        name_lbl = customtkinter.CTkLabel(self, text="Name:")
        self.add_label(name_lbl)
        self.name_entry = customtkinter.CTkEntry(self)
        self.add_input_widget(self.name_entry)

        # design
        design_lbl = customtkinter.CTkLabel(self, text="Design:")
        self.add_label(design_lbl)
        self.design_dropdown = customtkinter.CTkOptionMenu(self, values = ["", "Design1", "Design2", "Design3"])
        self.add_input_widget(self.design_dropdown)

        # design theme
        design_theme_lbl = customtkinter.CTkLabel(self, text="Theme:")
        self.add_label(design_theme_lbl)
        self.design_theme_dropdown = customtkinter.CTkOptionMenu(self, values = ["", "Theme1", "Theme2", "Theme3"])
        self.add_input_widget(self.design_theme_dropdown)

        # type
        type_lbl = customtkinter.CTkLabel(self, text="Type:")
        self.add_label(type_lbl)
        self.type_dropdown = customtkinter.CTkOptionMenu(self, values = ["", "Type1", "Type2", "Type3"])
        self.add_input_widget(self.type_dropdown)

        # sub-type
        sub_type_lbl = customtkinter.CTkLabel(self, text="Sub-type:")
        self.add_label(sub_type_lbl)
        self.sub_type_dropdown = customtkinter.CTkOptionMenu(self, values = ["", "Sub-type1", "Sub-type2", "Sub-type3"])
        self.add_input_widget(self.sub_type_dropdown)

        # colour
        colour_lbl = customtkinter.CTkLabel(self, text="Colour:")
        self.add_label(colour_lbl)
        self.colour_dropdown = customtkinter.CTkOptionMenu(self, values = ["", "Colour1", "Colour2", "Colour3"])
        self.add_input_widget(self.colour_dropdown)

    def add_label(self, lbl_widget):
        lbl_widget.grid(row=0, column=self.current_widget_num, padx=self.lbl_padx, pady=self.pady)
        self.current_widget_num += 1

    def add_input_widget(self, widget):
        widget.grid(row=0, column=self.current_widget_num, padx=self.widget_padx, pady=self.pady)
        self.current_widget_num += 1
        self.add_command_to_widget(widget) # update data table when filter is changed

    # update data table when filter is changed
    def add_command_to_widget(self, widget):
        cmd = lambda event: self.master.update_table()

        # if the widget is a CTkEntry then the command needs to be added differently to other widgets
        if isinstance(widget, customtkinter.CTkEntry):
            widget.bind("<KeyRelease>", command=cmd)
        else:
            widget.configure(command=cmd)

    def get_current_filter_values(self):
        return {
            "Item Type": self.product_component_switch.get(),
            "Name": self.name_entry.get(),
            "Design": self.design_dropdown.get(),
            "Theme": self.design_theme_dropdown.get(),
            "Type": self.type_dropdown.get(),
            "Sub-type": self.sub_type_dropdown.get(),
            "Colour": self.colour_dropdown.get()
        }
