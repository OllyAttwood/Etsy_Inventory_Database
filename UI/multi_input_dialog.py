import customtkinter
from UI.small_popup import SmallPopup
from UI import config
from UI.messagebox import MessageBox

class MultiInputDialog(SmallPopup):
    """
    An input pop-up window which gets and returns multiple inputs from the user (text) as a dictionary.
    The input widgets can be either entries or dropdown menus (ComboBox)
    get_user_input() should be called after creating a MultiInputDialog so that the input is returned to that function
    """

    def __init__(self, input_field_names, dropdown_menu_options_list, subject_name):
        """
        input_field_names is a list of the text that each label for each input will display.
        dropdown_menu_options_list is a list of the options for each dropdown menu to
            display. If None is provided for a given position, then an entry box will be
            displayed rather than a dropdown menu.
        subject_name is the type of thing that is being added e.g. Design, Product Type etc.
        """
        super().__init__()
        self.title(f"Add a {subject_name}")

        self.input_field_names = input_field_names
        self.dropdown_menu_options_list = dropdown_menu_options_list
        self.input_widgets = []
        self.subject_name = subject_name

        self.protocol("WM_DELETE_WINDOW", self.on_window_closed)

        self.display_widgets(input_field_names, dropdown_menu_options_list)

    def display_widgets(self, input_field_names, dropdown_menu_options_list):
        # loops through and creates a label/entry (or label/dropdown) pair of widgets for each required input
        for row, input_row_info in enumerate(zip(input_field_names, dropdown_menu_options_list)):
            input_text, dropdown_menu_options = input_row_info

            label = customtkinter.CTkLabel(self, text=input_text)
            self.grid_widget_with_padding(label, row=row, column=0)

            if dropdown_menu_options is None:
                input_widget = customtkinter.CTkEntry(self)
            else:
                input_widget = customtkinter.CTkComboBox(self, values=dropdown_menu_options)
            self.input_widgets.append(input_widget)
            self.grid_widget_with_padding(input_widget, row=row, column=1)

        # creates the add button
        add_button = customtkinter.CTkButton(self, text=f"Add {self.subject_name}", command=self.on_add_button_click)
        self.grid_widget_with_padding(add_button, row=len(input_field_names), column=1)

        self.input_widgets[0].focus_set()

    def grid_widget_with_padding(self, widget, row, column):
        widget.grid(row=row, column=column, padx=config.WIDGET_X_PADDING, pady=config.WIDGET_Y_PADDING)

    def on_add_button_click(self):
        """Stores the values in the input widgets, then closes the window"""
        self.input_dict = self.get_widget_inputs()

        # input validation
        if not self.validate_inputs():
            MessageBox("Input Error", "At least one of the input fields is empty!")
            return

        self.destroy_window()

    def get_user_input(self):
        """
        The function to call to wait until the user has entered and submitted input.
        Returns None if the window is closed by the user, otherwise returns a dictionary of the user inputs
        """
        self.master.wait_window(self) #waits until the input popup is closed

        return self.input_dict

    def get_widget_inputs(self):
        """Gets the current values the user has entered, as a dictionary"""
        input_dict = {}

        for input_name, input_widget in zip(self.input_field_names, self.input_widgets):
            input_dict[input_name] = input_widget.get()

        return input_dict

    def destroy_window(self):
        """Closes the popup window"""
        self.grab_release()
        self.destroy()

    def on_window_closed(self):
        """Function for when user closes the window rather than submitting their input"""
        self.input_dict = None
        self.destroy_window()

    def validate_inputs(self):
        """Ensures all the input fields have a value entered"""
        dict_values = list(self.input_dict.values())

        return "" not in dict_values
