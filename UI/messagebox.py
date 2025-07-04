import customtkinter
from UI.small_popup import SmallPopup

class MessageBox(SmallPopup):
    """A very simple pop-up window which displays a message to the user"""
    def __init__(self, title, message):
        super().__init__()
        self.title(title)
        self.geometry("300x150")

        #keep widgets in centre during resizing
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #widgets
        message_label = customtkinter.CTkLabel(self, text=message, wraplength=250)
        message_label.grid(row=0, column=0)

        ok_button = customtkinter.CTkButton(self, text="OK", command=self.release_focus_and_hide)
        ok_button.grid(row=1, column=0)
