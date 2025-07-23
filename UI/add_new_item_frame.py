import customtkinter
from UI.spinbox import Spinbox
from UI.multi_input_dialog import MultiInputDialog
from tkinter import NORMAL, DISABLED
from UI.messagebox import MessageBox
import sqlite3
from UI.small_popup import SmallPopup
from UI import config
from UI.utilities import add_empty_string_option_and_alphabetise

class AddNewItemFrame(customtkinter.CTkFrame):
    def __init__(self, master, presenter, tab_view):
        super().__init__(master)

        self.manage_component_window = None
        self.widget_grid = []
        self.component_compatible_widgets = [] # widgets which should not be greyed out when adding a component
        self.presenter = presenter
        self.tab_view = tab_view
        self.centre_frame = customtkinter.CTkFrame(self) # needed to make widgets display in centre of screen
        self.centre_frame.grid(row=0, column=0)
        self.grid_columnconfigure(0, weight=1) # centralises the centre_frame
        # values for the optionmenus / comboboxes
        self.load_menu_options_values()
        # input field text for the input dialogs
        self.design_input_field_names = ["Name", "Theme"]
        self.product_type_input_field_names = ["Name", "Type", "Sub-Type"]

        # item type
        product_component_lbl_str = "Item Type:"
        product_component_vals = ["Product", "Component"]
        self.product_component_switch = customtkinter.CTkSegmentedButton(self.centre_frame, values=product_component_vals,
                                                                         command=self.change_product_widgets_state)
        self.product_component_switch.set(product_component_vals[0])
        self.widget_grid.append([product_component_lbl_str, self.product_component_switch])
        self.component_compatible_widgets.append(self.product_component_switch)

        # name
        name_lbl_str = "Name:"
        self.name_entry = customtkinter.CTkEntry(self.centre_frame)
        self.widget_grid.append([name_lbl_str, self.name_entry])
        self.component_compatible_widgets.append(self.name_entry)

        # design
        design_lbl_str = "Design:"
        self.design_dropdown = customtkinter.CTkOptionMenu(self.centre_frame, values=self.design_options)
        new_design_button = customtkinter.CTkButton(self.centre_frame, text="Add New Design... ",
                                                    command=self.on_design_button_click)
        self.widget_grid.append([design_lbl_str, self.design_dropdown, new_design_button])

        # colour
        colour_lbl_str = "Colour:"
        self.colour_dropdown = customtkinter.CTkComboBox(self.centre_frame, values=self.colour_options)
        self.widget_grid.append([colour_lbl_str, self.colour_dropdown])

        # type
        type_lbl_str = "Type:"
        self.type_dropdown = customtkinter.CTkOptionMenu(self.centre_frame, values=self.type_options)
        new_type_button = customtkinter.CTkButton(self.centre_frame, text="Add New Type... ",
                                                  command=self.on_type_button_click)
        self.widget_grid.append([type_lbl_str, self.type_dropdown, new_type_button])

        # stock
        stock_lbl_str = "Stock:"
        self.stock_spinbox = Spinbox(self.centre_frame)
        self.widget_grid.append([stock_lbl_str, self.stock_spinbox])
        self.component_compatible_widgets.append(self.stock_spinbox)

        # low stock
        low_stock_lbl_str = "Low Stock Warning:"
        self.low_stock_spinbox = Spinbox(self.centre_frame)
        self.widget_grid.append([low_stock_lbl_str, self.low_stock_spinbox])
        self.component_compatible_widgets.append(self.low_stock_spinbox)

        # components
        components_lbl_str = "Components:"
        components_button = customtkinter.CTkButton(self.centre_frame, text="Manage Components...",
                                                    command=self.component_button_click)
        self.widget_grid.append([components_lbl_str, components_button])

        #loop through widget_grid, adding widgets
        for row_num, row_widgets in enumerate(self.widget_grid):
            for col_num, widget in enumerate(row_widgets):
                #create label widget from label strings
                if col_num == 0:
                    widget = customtkinter.CTkLabel(self.centre_frame, text=widget)

                widget.grid(row=row_num, column=col_num, padx=config.WIDGET_X_PADDING/2, pady=config.WIDGET_Y_PADDING/2)

        # add new item button
        add_item_button = customtkinter.CTkButton(self.centre_frame, text="Add Item",
                                                  command=self.on_add_item_button_click)
        row_num += 1 #cheeky reuse of loop variable
        add_item_button.grid(row=row_num, column=1, padx=config.WIDGET_X_PADDING, pady=config.WIDGET_Y_PADDING*2)

    def component_button_click(self):
        """Opens the component selection window - creates a new one if it doesn't already exist"""
        if not self.manage_component_window:
            self.manage_component_window = ManageComponentWindow(self.presenter)
        else:
            self.manage_component_window.reappear()

    def load_menu_options_values(self):
        """Gets the existing values for the comboboxes/optionmenus"""
        self.design_options = self.presenter.get_product_designs()
        self.colour_options = self.presenter.get_product_colours()
        self.type_options = self.presenter.get_product_type_names()

        add_empty_string_option_and_alphabetise([self.design_options, self.colour_options, self.type_options])

    def on_add_button_click(self, option_menu_to_update, input_field_names, dropdown_menu_options_list, subject_name, save_func):
        """Adds a new option to an optionmenu from the user input, and saves it to database"""
        input_dialog = MultiInputDialog(input_field_names, dropdown_menu_options_list, subject_name)
        input_dict = input_dialog.get_user_input()

        if input_dict: # if input_dict == None then user closed the dialog
            user_inputs = [input_dict[key] for key in input_field_names]
            try:
                save_func(*user_inputs) # unpacks the list into individual variables so the function can accept it
            except sqlite3.IntegrityError: # catch error where duplicate 'name' has been entered by the user
                self.create_name_error_popup()
                return
            new_option = input_dict["Name"]
            self.add_new_option_to_optionmenu(new_option, option_menu_to_update)
            option_menu_to_update.set(new_option)

    def add_new_option_to_optionmenu(self, new_option, optionmenu):
        """Updates the optionmenu with a new option at the end of the list"""
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

    def on_add_item_button_click(self):
        """Save the new item to the database"""
        item_type = self.product_component_switch.get()

        if item_type == "Product":
            name = self.name_entry.get()
            design = self.design_dropdown.get()
            colour = self.colour_dropdown.get()
            product_type = self.type_dropdown.get()
            stock = self.stock_spinbox.get()
            low_stock_warning = self.low_stock_spinbox.get()
            try:
                components = self.manage_component_window.get_selected_components()
            except AttributeError: # ManageComponentWindow was never opened by the user
                components = []
            except TypeError: # something other than a number entered into a ManageComponentWindow spinbox
                MessageBox("Input Error", "At least one of the component quantity input fields is not an integer!")
                return

            # input validation
            if not self.validate_inputs([name, design, colour, product_type], [stock, low_stock_warning], components):
                MessageBox("Input Error", "At least one of the input fields is either empty or in an incorrect format!")
                return

            try:
                self.presenter.save_new_product(name, design, colour, product_type, stock, low_stock_warning, components)
            except sqlite3.IntegrityError: # catch error where duplicate 'name' has been entered by the user
                self.create_name_error_popup()
                return

        elif item_type == "Component":
            name = self.name_entry.get()
            stock = self.stock_spinbox.get()
            low_stock_warning = self.low_stock_spinbox.get()

            # input validation
            if not self.validate_inputs([name], [stock, low_stock_warning], []):
                MessageBox("Input Error", "At least one of the input fields is either empty or an incorrect format!")
                return

            try:
                self.presenter.save_new_component(name, stock, low_stock_warning)
            except sqlite3.IntegrityError: # catch error where duplicate 'name' has been entered by the user
                self.create_name_error_popup()
                return

        #reloads UI elements that need updating after new item has been added
        self.tab_view.reload_all_frames()

    def create_name_error_popup(self):
        """Creates and shows an error message for when a product/component already exists with the same name"""
        MessageBox("Name Error", "That name is already in use!")

    def validate_inputs(self, non_empty_strings, spinbox_strings, components_list):
        """Validates the inputs before doing anything with them.
        non_empty_strings is a list of the strings that should be checked for being non-empty.
        spinbox_strings is a list of strings obtained from the spinboxes that should be checked
            for being not None (this implies the string correctly represents an integer - see Spinbox.get()).
        component_list is a list of tuples (component name and quantity) that should be checked for all
            quantities being not None, as in spinbox_strings
        """
        # check non_empty_strings
        if "" in non_empty_strings:
            return False

        # check spinbox_strings
        if None in spinbox_strings:
            return False

        # check components_list
        component_quantity_index = 1
        if None in [name_and_quantity[component_quantity_index] for name_and_quantity in components_list]:
            return False

        # if all the inputs are valid
        return True

    def on_design_button_click(self):
        """Opens the dialog to add a new design"""
        themes = self.presenter.get_product_themes()
        add_empty_string_option_and_alphabetise([themes])
        self.on_add_button_click(self.design_dropdown, self.design_input_field_names, [None, themes],
                                 "Design", self.presenter.save_new_design)

    def on_type_button_click(self):
        """Opens the dialog to add a new design"""
        types = self.presenter.get_product_types()
        sub_types = self.presenter.get_product_sub_types()
        add_empty_string_option_and_alphabetise([types, sub_types])
        self.on_add_button_click(self.type_dropdown, self.product_type_input_field_names,
                                 [None, types, sub_types], "Product Type",
                                 self.presenter.save_new_product_type)



class ManageComponentWindow(SmallPopup):
    """The pop-up window to display all the available components, with spinboxes to select quantities.
    Shows an error message if there are no saved components.
    """
    def __init__(self, presenter):
        super().__init__()
        self.title("Manage Components")
        self.presenter = presenter
        self.spinboxes = []

        # display component info
        self.component_names = self.presenter.get_component_names()
        self.component_names.sort(key=str.lower) # alphabetise list

        if len(self.component_names) > 0: # check whether there are any components to show
            self.display_components([[com_name, 0] for com_name in self.component_names])
        else:
            self.display_no_components_message()

    def reappear(self):
        """Makes the window re-appear, with the same quantities as previously selected"""
        self.deiconify()
        self.lock_at_front()

    def display_components(self, component_data):
        """Sets up all the UI widgets"""
        self.geometry("400x400")
        scrollable_frame = customtkinter.CTkScrollableFrame(self)
        scrollable_frame.grid(row=0, column=0, sticky="nsew")

        scrollable_frame.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        #loop through component_data, adding widgets
        for row_num, component_row in enumerate(component_data):
            # label
            label = customtkinter.CTkLabel(scrollable_frame, text=component_row[0])
            label.grid(row=row_num, column=0, padx=config.WIDGET_X_PADDING, pady=config.WIDGET_Y_PADDING/2)

            # spinbox
            spinbox_frame = customtkinter.CTkFrame(scrollable_frame)
            spinbox_frame.grid(row=row_num, column=1)
            stock_spinbox = Spinbox(spinbox_frame, initial_value=component_row[1])
            stock_spinbox.grid(row=0, column=0, padx=config.WIDGET_X_PADDING, pady=config.WIDGET_Y_PADDING/2)
            self.spinboxes.append(stock_spinbox)

        close_button = customtkinter.CTkButton(self, text="Close", command=self.release_focus_and_hide)
        row_num += 1 # using the loop variable - cheeky
        close_button.grid(row=1, column=0, columnspan=2, padx=config.WIDGET_X_PADDING, pady=config.WIDGET_Y_PADDING)

    def get_selected_components(self):
        """Returns a list of tuples of the component names of which more than 0 quantity has been selected, and their quantities
        e.g. [('Jump ring - large', 4), ('Earring hook', 2), ('Earring back', 2)]
        """
        component_list = []

        for component_name, component_spinbox in zip(self.component_names, self.spinboxes):
            quantity = component_spinbox.get()

            if quantity > 0:
                component_list.append((component_name, quantity))

        return component_list

    def display_no_components_message(self):
        """Show an error message for when there are no saved components to display"""
        self.geometry("400x200")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        label = customtkinter.CTkLabel(self, text="No components have been added to the database yet!")
        label.grid(row=0, column=0)

"""
-------------------------------------------------------------------------------------------------------------------------------------------------------------

fix error when adding a new product without all fields filled in
    also check other edge cases like tha
    ADD INPUT VALIDATION (CHECK ALL INPUTS ARE NOT EMPTY IF NECESSARY)
        validate add design/type popups (after changing to include dropdowns if necessary)
        catch database errors when user inserts (duplicate name error already done in AddNewItemFrame?)

unit tests

update all code to use leading underscore for all private function names

tidy up UI
    <PROBABLY NOT NEEDED> add popup confirmation boxes when adding items, updating stock levels etc
    change background colour of central frames?

add comments to functions/classes

add README
"""
