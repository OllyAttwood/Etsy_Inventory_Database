from UI.small_popup import SmallPopup
import customtkinter

class Splash(SmallPopup):
    """A splash screen which covers the whole window while waiting for UI to load"""
    FONT_SIZE = 50

    def __init__(self, master, program_startup=False):
        super().__init__()

        # remove the title bar of the window
        self.wm_attributes('-type', 'splash')

        # size and position of splash screen
        root = master.winfo_toplevel()
        width = root.winfo_width()
        height = root.winfo_height()
        x = root.winfo_rootx() # matches the position of root window
        y = root.winfo_rooty()
        self.geometry(f"{width}x{height}+{x}+{y}")

        # widgets and grid configuring
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        splash_text_dict = {
            True: "Welcome to Product Database\n\nLoading...",
            False: "Updating database..."
        }

        label = customtkinter.CTkLabel(
            self,
            text=splash_text_dict[program_startup],
            font=(None, self.FONT_SIZE)
        )
        label.grid(row=0, column=0)

    def destroy(self, delay=10, step_size=0.05):
        """Destroys the splash screen, fading it out before closing"""
        alpha = self.attributes("-alpha")

        # slowly reduces the alpha until it is close to 0, then destroys the window
        if alpha > step_size:
            self.attributes("-alpha", alpha - step_size)
            self.after(delay, self.destroy)
        else:
            super().destroy()
