import customtkinter
from tkinter import StringVar, DISABLED, NORMAL

class FilterBarFrame(customtkinter.CTkFrame):
    def __init__(self, master, design_options, theme_options, type_options, sub_type_options, colour_options):
        super().__init__(master)
        self.master = master

        #add the empty option to the dropdown menus as the default
        self.add_empty_string_option([design_options, theme_options, type_options, sub_type_options, colour_options])

        # padding vars
        self.lbl_padx = 10
        self.widget_padx= (0,10)
        self.pady = 10 # pady for both labels and other widgets
        # widget position counter
        self.current_widget_num = 0
        self.input_widgets = []

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
        self.design_dropdown = customtkinter.CTkOptionMenu(self, values=design_options)
        self.add_input_widget(self.design_dropdown)

        # design theme
        design_theme_lbl = customtkinter.CTkLabel(self, text="Theme:")
        self.add_label(design_theme_lbl)
        self.design_theme_dropdown = customtkinter.CTkOptionMenu(self, values=theme_options)
        self.add_input_widget(self.design_theme_dropdown)

        # type
        type_lbl = customtkinter.CTkLabel(self, text="Type:")
        self.add_label(type_lbl)
        self.type_dropdown = customtkinter.CTkOptionMenu(self, values=type_options)
        self.add_input_widget(self.type_dropdown)

        # sub-type
        sub_type_lbl = customtkinter.CTkLabel(self, text="Sub-type:")
        self.add_label(sub_type_lbl)
        self.sub_type_dropdown = customtkinter.CTkOptionMenu(self, values=sub_type_options)
        self.add_input_widget(self.sub_type_dropdown)

        # colour
        colour_lbl = customtkinter.CTkLabel(self, text="Colour:")
        self.add_label(colour_lbl)
        self.colour_dropdown = customtkinter.CTkOptionMenu(self, values=colour_options)
        self.add_input_widget(self.colour_dropdown)

        #initialise the filter state dictionary - to be used to check if the filters have actually been changed
        self.current_filter_values = self.get_current_filter_values()

    def add_label(self, lbl_widget):
        lbl_widget.grid(row=0, column=self.current_widget_num, padx=self.lbl_padx, pady=self.pady)
        self.current_widget_num += 1

    def add_input_widget(self, widget):
        widget.grid(row=0, column=self.current_widget_num, padx=self.widget_padx, pady=self.pady)
        self.current_widget_num += 1
        self.add_command_to_widget(widget) # update data table when filter is changed
        self.input_widgets.append(widget)

    def on_filter_widget_update(self, event):
        """Function to be run when any of the filter widgets have been updated, regardless of whether their values have actually been changed"""
        new_filter_values = self.get_current_filter_values()

        #check whether table needs updating
        if new_filter_values != self.current_filter_values:
            #updates table after applying new filters and keeps self.current_filter_values up-to-date
            self.master.update_table(new_filter_values)
            self.current_filter_values = new_filter_values

            #greys out filter widgets which aren't applicable to components
            if event == "Component":
                self.change_product_widgets_state(DISABLED)
            elif event == "Product":
                self.change_product_widgets_state(NORMAL)

    # update data table when filter is changed
    def add_command_to_widget(self, widget):
        # if the widget is a CTkEntry then the command needs to be added differently to other widgets
        if isinstance(widget, customtkinter.CTkEntry):
            widget.bind("<KeyRelease>", command=self.on_filter_widget_update)
        else:
            widget.configure(command=self.on_filter_widget_update)

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

    def add_empty_string_option(self, list_of_options_lists):
        """Inserts an empty string at the beginning of each of the lists, to use as the default (unfiltered) value for a dropdown mennu"""
        for options in list_of_options_lists:
            options.insert(0, "")

    def change_product_widgets_state(self, new_state):
        """Sets whether the widgets that are used for filtering just products (not components) should be greyed out or not"""
        component_compatible_widgets = [self.product_component_switch, self.name_entry] #widgets that shouldn't be greyed out ever
        for widget in self.input_widgets:
            if widget not in component_compatible_widgets:
                widget.configure(state=new_state)
