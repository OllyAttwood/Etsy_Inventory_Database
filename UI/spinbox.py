import customtkinter
from typing import Callable, Union

class Spinbox(customtkinter.CTkFrame):
    """A small widget to increase/decrease a quantity.
    This class is modified from https://customtkinter.tomschimansky.com/tutorial/spinbox
    """
    
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: int = 1,
                 command: Callable = None,
                 initial_value=0,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command
        self.initial_value = initial_value

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        subtract_text = "-"
        self.subtract_button = customtkinter.CTkButton(self, text=subtract_text, width=height-6, height=height-6,
                                                       command=lambda: self.button_callback(subtract_text))
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = customtkinter.CTkEntry(self, width=width-(2*height), height=height-6, border_width=0, justify="center")
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        add_text = "+"
        self.add_button = customtkinter.CTkButton(self, text=add_text, width=height-6, height=height-6,
                                                  command=lambda: self.button_callback(add_text))
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        # default value
        self.entry.insert(0, str(self.initial_value))

    def button_callback(self, add_or_subtract):
        """Increases or decreases the value in the Spinbox"""
        if self.command is not None:
            self.command(),
        try:
            value = int(self.entry.get())

            if add_or_subtract == "+":
                value += self.step_size
            else:
                value -= self.step_size

            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def get(self) -> Union[int, None]:
        try:
            return int(self.entry.get())
        except ValueError:
            return None

    def set(self, value: int):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(int(value)))
