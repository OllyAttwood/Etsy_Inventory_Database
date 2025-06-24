import customtkinter
from UI.spinbox import Spinbox
from UI.multi_input_dialog import MultiInputDialog
from tkinter import NORMAL, DISABLED

class AddNewItemFrame(customtkinter.CTkFrame):
    def __init__(self, master, presenter):
        super().__init__(master)

        self.manage_component_window = None
        self.widget_grid = []
        self.component_compatible_widgets = [] # widgets which should not be greyed out when adding a component
        self.presenter = presenter
        # values for the optionmenus / comboboxes
        self.load_menu_options_values()
        # input field text for the input dialogs
        self.design_input_field_names = ["Name", "Theme"]
        self.product_type_input_field_names = ["Name", "Type", "Sub-Type"]

        # item type
        product_component_lbl_str = "Item Type:"
        product_component_vals = ["Product", "Component"]
        product_component_switch = customtkinter.CTkSegmentedButton(self, values=product_component_vals, command=self.change_product_widgets_state)
        product_component_switch.set(product_component_vals[0])
        self.widget_grid.append([product_component_lbl_str, product_component_switch])
        self.component_compatible_widgets.append(product_component_switch)

        # name
        name_lbl_str = "Name:"
        name_entry = customtkinter.CTkEntry(self)
        self.widget_grid.append([name_lbl_str, name_entry])
        self.component_compatible_widgets.append(name_entry)

        # design
        design_lbl_str = "Design:"
        design_dropdown = customtkinter.CTkOptionMenu(self, values=self.design_options)
        design_button_command = lambda: self.on_add_button_click(design_dropdown, self.design_input_field_names,
                                                                 "Design", self.presenter.save_new_design)
        new_design_button = customtkinter.CTkButton(self, text="Add new design... ", command=design_button_command)
        self.widget_grid.append([design_lbl_str, design_dropdown, new_design_button])

        # colour
        colour_lbl_str = "Colour:"
        colour_dropdown = customtkinter.CTkComboBox(self, values=self.colour_options)
        self.widget_grid.append([colour_lbl_str, colour_dropdown])

        # type
        type_lbl_str = "Type:"
        type_dropdown = customtkinter.CTkOptionMenu(self, values=self.type_options)
        type_button_command = lambda: self.on_add_button_click(type_dropdown, self.product_type_input_field_names,
                                                               "Product Type", self.presenter.save_new_product_type)
        new_type_button = customtkinter.CTkButton(self, text="Add new type... ", command=type_button_command)
        self.widget_grid.append([type_lbl_str, type_dropdown, new_type_button])

        # stock
        stock_lbl_str = "Stock:"
        stock_spinbox = Spinbox(self)
        self.widget_grid.append([stock_lbl_str, stock_spinbox])
        self.component_compatible_widgets.append(stock_spinbox)

        # low stock
        low_stock_lbl_str = "Low Stock Warning:"
        low_stock_spinbox = Spinbox(self)
        self.widget_grid.append([low_stock_lbl_str, low_stock_spinbox])
        self.component_compatible_widgets.append(low_stock_spinbox)

        # components
        components_lbl_str = "Components:"
        components_button = customtkinter.CTkButton(self, text="Manage components...",
                                                    command=self.component_button_click)
        self.widget_grid.append([components_lbl_str, components_button])

        #loop through widget_grid, adding widgets
        for row_num, row_widgets in enumerate(self.widget_grid):
            for col_num, widget in enumerate(row_widgets):
                #create label widget from label strings
                if col_num == 0:
                    widget = customtkinter.CTkLabel(self, text=widget)

                widget.grid(row=row_num, column=col_num)

        # add new item button
        add_item_button = customtkinter.CTkButton(self, text="Add item")
        row_num += 1 #cheeky reuse of loop variable
        add_item_button.grid(row=row_num, column=1)

    def component_button_click(self):
        if not self.manage_component_window:
            self.manage_component_window = ManageComponentWindow(self.presenter)
        else:
            self.manage_component_window.reappear()

    def load_menu_options_values(self):
        self.design_options = self.presenter.get_product_designs()
        self.colour_options = self.presenter.get_product_colours()
        self.type_options = self.presenter.get_product_types()

        self.add_empty_string_option([self.design_options, self.colour_options, self.type_options])

    def add_empty_string_option(self, list_of_options_lists):
        """Inserts an empty string at the beginning of each of the lists, to use as the default (unfiltered) value for a dropdown mennu"""
        for options in list_of_options_lists:
            options.insert(0, "")

    def on_add_button_click(self, option_menu_to_update, input_field_names, subject_name, save_func):
        """Adds a new option to an optionmenu from the user input, and saves it to database"""
        input_dialog = MultiInputDialog(input_field_names, subject_name)
        input_dict = input_dialog.get_user_input()

        if input_dict: # if input_dict == None then user closed the dialog
            user_inputs = [input_dict[key] for key in input_field_names]
            save_func(*user_inputs) # unpacks the list into individual variables so the function can accept it
            self.add_new_option_to_optionmenu(input_dict["Name"], option_menu_to_update)

    def add_new_option_to_optionmenu(self, new_option, optionmenu):
        current_options = list(optionmenu._values)  # _values is the internal list of options
        current_options.append(new_option)
        optionmenu.configure(values=current_options)

    def change_product_widgets_state(self, selected_item_type):
        """Disable any non-applicable widgets when 'Components' is selected, otherwise enable them all"""
        new_state = None

        if selected_item_type == "Product":
            new_state = NORMAL
        elif selected_item_type == "Component": #disable unnecessary widgets
            new_state = DISABLED

        for row in self.widget_grid:
            for widget in row:
                # if not a component widget and also is an actual widget (not a string)
                if widget not in self.component_compatible_widgets and not isinstance(widget, str):
                    widget.configure(state=new_state)



class ManageComponentWindow(customtkinter.CTkToplevel):
    def __init__(self, presenter):
        super().__init__()
        self.title("Manage Components")

        self.presenter = presenter

        # lock popup at front
        self.attributes("-topmost", "true")
        # make main window unclickable until popup is closed
        self.lock_at_front()

        # override the exit button as exiting produces an error, so we just
        # hide the window and restore it if necessary
        self.protocol("WM_DELETE_WINDOW", self.release_focus_and_hide)

        # display component info
        component_names = self.presenter.get_component_names()
        self.display_components([[com_name, 0] for com_name in component_names])

    # hides window
    def release_focus_and_hide(self):
        self.grab_release()
        self.withdraw()

    # make main window unclickable until popup is closed
    def lock_at_front(self):
        self.wait_visibility() # https://raspberrypi.stackexchange.com/a/105522
        self.grab_set()

    def reappear(self):
        self.deiconify()
        self.lock_at_front()

    def display_components(self, component_data):
        #loop through component_data, adding widgets
        for row_num, component_row in enumerate(component_data):
            label = customtkinter.CTkLabel(self, text=component_row[0])
            label.grid(row=row_num, column=0)
            stock_spinbox = Spinbox(self, initial_value=component_row[1])
            stock_spinbox.grid(row=row_num, column=1)

        close_button = customtkinter.CTkButton(self, text="Close", command=self.release_focus_and_hide)
        row_num += 1 # using the loop variable - cheeky
        close_button.grid(row=row_num, column=0)
