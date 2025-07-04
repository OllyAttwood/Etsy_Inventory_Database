import customtkinter

class MessageBox(customtkinter.CTkToplevel):
    """A very simple pop-up window which displays a message to the user"""
    def __init__(self, title, message):
        super().__init__()
        self.title(title)
        self.geometry("300x150")

        # lock popup at front
        self.attributes("-topmost", "true")
        # make main window unclickable until popup is closed
        self.lock_at_front()

        # override the exit button
        self.protocol("WM_DELETE_WINDOW", self.close_window)

        #keep widgets in centre during resizing
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #widgets
        message_label = customtkinter.CTkLabel(self, text=message, wraplength=250)
        message_label.grid(row=0, column=0)

        ok_button = customtkinter.CTkButton(self, text="OK", command=self.close_window)
        ok_button.grid(row=1, column=0)

    def close_window(self):
        self.grab_release() # release focus
        self.withdraw()
        self.destroy()

    # make main window unclickable until popup is closed
    def lock_at_front(self):
        self.wait_visibility() # https://raspberrypi.stackexchange.com/a/105522
        self.grab_set()
