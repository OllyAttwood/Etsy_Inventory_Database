import customtkinter

class SmallPopup(customtkinter.CTkToplevel):
    """
    A class for other classes to inherit, which want to be small pop-up windows, locked
    at the front of the program.
    """

    def __init__(self):
        super().__init__()

        # lock popup at front
        self.attributes("-topmost", "true")
        # make main window unclickable until popup is closed
        self.lock_at_front()

        # override the exit button as exiting produces an error, so we just
        # hide the window and restore it if necessary
        self.protocol("WM_DELETE_WINDOW", self.release_focus_and_hide)

    def release_focus_and_hide(self):
        """Hides the window"""
        self.grab_release()
        self.withdraw()

    def lock_at_front(self):
        """Makes main window unclickable until popup is closed"""
        self.wait_visibility() # https://raspberrypi.stackexchange.com/a/105522
        self.grab_set()

    def centre_popup(self):
        """Position the popup in the centre of the screen"""
        # force UI to fully update before the dimensions are calculated
        self.update_idletasks()

        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.geometry(f"{width}x{height}+{x}+{y}")
