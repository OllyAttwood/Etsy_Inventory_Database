import customtkinter
from UI.small_popup import SmallPopup
from UI import config

class MultiInputDialog(SmallPopup):
    """An input pop-up window which gets and returns multiple inputs from the user (text) as a dictionary.
    get_user_input() should be called after creating a MultiInputDialog so that the input is returned to that function
    """
    def __init__(self, input_text_list, subject_name): #subject_name is the type of thing that is being added e.g. Design, Product Type etc
        super().__init__()
        self.title(f"Add a {subject_name}")

        self.input_text_list = input_text_list
        self.entry_widgets = []
        self.subject_name = subject_name

        self.protocol("WM_DELETE_WINDOW", self.on_window_closed)

        self.display_widgets(input_text_list)

    def display_widgets(self, input_text_list):
        # loops through and creates a label/entry pair of widgets for each required input
        for row, input_text in enumerate(input_text_list):
            label = customtkinter.CTkLabel(self, text=input_text)
            label.grid(row=row, column=0, padx=config.WIDGET_X_PADDING, pady=config.WIDGET_Y_PADDING)

            entry = customtkinter.CTkEntry(self)
            self.entry_widgets.append(entry)
            entry.grid(row=row, column=1, padx=config.WIDGET_X_PADDING, pady=config.WIDGET_Y_PADDING)

        # creates the add button
        add_button = customtkinter.CTkButton(self, text=f"Add {self.subject_name}", command=self.on_add_button_click)
        add_button.grid(row=len(input_text_list), column=1, padx=config.WIDGET_X_PADDING, pady=config.WIDGET_Y_PADDING)

    def on_add_button_click(self):
        """Stores the values in the entry fields, then closes the window"""
        self.input_dict = self.get_entry_inputs()
        self.destroy_window()

    def get_user_input(self):
        """The function to call to wait until the user has entered and submitted input.
        Returns None if the window is closed by the user, otherwise returns a dictionary of the user inputs"""
        self.master.wait_window(self) #waits until the input popup is closed

        return self.input_dict

    def get_entry_inputs(self):
        """Gets the current values the user has entered, as a dictionary"""
        input_dict = {}

        for input_name, entry in zip(self.input_text_list, self.entry_widgets):
            input_dict[input_name] = entry.get()

        return input_dict

    def destroy_window(self):
        """Closes the popup window"""
        self.grab_release()
        self.destroy()

    def on_window_closed(self):
        """Function for when user closes the window rather than submitting their input"""
        self.input_dict = None
        self.destroy_window()
