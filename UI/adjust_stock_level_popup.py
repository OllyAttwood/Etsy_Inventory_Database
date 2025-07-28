import customtkinter
from UI.spinbox import Spinbox
from UI.small_popup import SmallPopup
from UI import config
from UI.messagebox import MessageBox

class AdjustStockLevelPopup(SmallPopup):
    """A popup window to adjust the stock level of a given item"""

    def __init__(self, item_name, item_id, item_type, presenter, tab_view):
        super().__init__()
        self.title("Adjust Stock Level")
        self.geometry("500x250")

        self.item_name = item_name
        self.item_id = item_id
        self.item_type = item_type
        self.presenter = presenter
        self.tab_view = tab_view

        #keep widgets in centre during resizing
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #widgets
        text_to_show = f"How much do you want to increase/decrease the stock level of {item_name}? (e.g. -2 will decrease stock level by 2)"
        text_label = customtkinter.CTkLabel(self, text=text_to_show,
                                            wraplength=200)
        text_label.grid(row=0, column=0)

        self.spinbox = Spinbox(self)
        self.spinbox.grid(row=1, column=0)

        ok_button = customtkinter.CTkButton(self, text="OK", command=self.apply_change_and_close_window)
        ok_button.grid(row=2, column=0, pady=config.WIDGET_Y_PADDING)

    def close_window(self):
        """Closes the window and releases the focus (as the pop-up initially takes the focus so no other window can be interacted with)"""
        self.grab_release() # release focus
        self.withdraw()
        self.destroy()

    def apply_change_and_close_window(self):
        """
        Applies the stock level change specified by the user (if a product stock is
        being decreased, a pop-up asks if the stock level of the product's components
        should also be reduced i.e. if the product has been sold so the component are
        no longer available)
        """
        # validate inputs first
        if not self.validate_inputs():
            MessageBox("Input Error", "Only integers can be entered!")
            return

        stock_level_change = self.spinbox.get()

        if stock_level_change > 0:
            # increase stock
            if self.item_type == "Product":
                self.presenter.update_product_stock_level(self.item_id, stock_level_change)
                self.tab_view.reload_all_frames() # reloads UI to show new values
            elif self.item_type == "Component":
                self.presenter.update_component_stock_level(self.item_id, stock_level_change)
                self.tab_view.reload_all_frames(display_components_in_view_items_frame=True) # reloads UI to show new values
        elif stock_level_change < 0:
            if self.item_type == "Product":
                # ask user if they want to automatically reduce the stock level of the product's components too
                ReduceComponentStockLevelPopup(self.item_id, self.item_type, stock_level_change, self.presenter, self.tab_view)
            elif self.item_type == "Component":
                # increase stock
                self.presenter.update_component_stock_level(self.item_id, stock_level_change)
                self.tab_view.reload_all_frames(display_components_in_view_items_frame=True) # reloads UI to show new values

        # if stock_level_change == 0 then do nothing other tan close the window

        self.close_window()

    def validate_inputs(self):
        """Checks if the inputs are valid, returns False if invalid, otherwise True"""
        spinbox_value = self.spinbox.get()

        return spinbox_value is not None

class ReduceComponentStockLevelPopup(SmallPopup):
    """This window asks the user if they also want to reduce the stock levels of the components that the item is made with"""
    def __init__(self, item_id, item_type, stock_level_change, presenter, tab_view):
        super().__init__()
        self.title("Reduce Component Stock Levels?")
        self.geometry("300x150")

        self.item_id = item_id
        self.item_type = item_type
        self.stock_level_change = stock_level_change
        self.presenter = presenter
        self.tab_view = tab_view

        # widgets
        central_frame = customtkinter.CTkFrame(self) # frame to keep all widgets in centre without stretching them
        central_frame.grid(row=0, column=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        text_to_show = f"Do you also want to reduce the stock levels of the components that are used to create this product?"
        text_label = customtkinter.CTkLabel(central_frame, text=text_to_show,
                                            wraplength=200)
        text_label.grid(row=0, column=0, columnspan=2)

        yes_button = customtkinter.CTkButton(central_frame, text="Yes", command=self.on_yes_button_click)
        yes_button.grid(row=1, column=0)

        no_button = customtkinter.CTkButton(central_frame, text="No", command=self.on_no_button_click)
        no_button.grid(row=1, column=1)

    def lock_at_front(self):
        """Make main window unclickable until pop-up is closed"""
        self.wait_visibility() # https://raspberrypi.stackexchange.com/a/105522
        self.grab_set()

    def on_no_button_click(self):
        """Update just the product's stock level, then close the pop-up and reload the UI"""
        if self.item_type == "Product":
            self.presenter.update_product_stock_level(self.item_id, self.stock_level_change)
        elif self.item_type == "Component":
            self.presenter.update_component_stock_level(self.item_id, self.stock_level_change)
        self.release_focus_and_hide()
        self.tab_view.reload_all_frames() # reloads UI to show new values

    def on_yes_button_click(self):
        """
        Update the product's stock level, as well as its components' stock levels, then
        close the pop-up and reload the UI
        """
        self.presenter.update_product_stock_level_and_its_components_stock_levels(self.item_id, self.stock_level_change)
        self.release_focus_and_hide()
        self.tab_view.reload_all_frames() # reloads UI to show new values
