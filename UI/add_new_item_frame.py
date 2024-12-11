import customtkinter
from spinbox import Spinbox

class AddNewItemFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.manage_component_window = None
        self.widget_grid = []

        # item type
        product_component_lbl_str = "Item Type:"
        product_component_vals = ["Product", "Component"]
        product_component_switch = customtkinter.CTkSegmentedButton(self, values=product_component_vals)
        product_component_switch.set(product_component_vals[0])
        self.widget_grid.append([product_component_lbl_str, product_component_switch])

        # name
        name_lbl_str = "Name:"
        name_entry = customtkinter.CTkEntry(self)
        self.widget_grid.append([name_lbl_str, name_entry])

        # theme
        theme_lbl_str = "Theme:"
        theme_dropdown = customtkinter.CTkOptionMenu(self, values = ["", "Theme1", "Theme2", "Theme3"])
        new_theme_button = customtkinter.CTkButton(self, text="Add new theme... ")
        self.widget_grid.append([theme_lbl_str, theme_dropdown, new_theme_button])

        # design
        design_lbl_str = "Design:"
        design_dropdown = customtkinter.CTkOptionMenu(self, values = ["", "Design1", "Design2", "Design3"])
        new_design_button = customtkinter.CTkButton(self, text="Add new design... ")
        self.widget_grid.append([design_lbl_str, design_dropdown, new_design_button])

        # colour
        colour_lbl_str = "Colour:"
        colour_dropdown = customtkinter.CTkOptionMenu(self, values = ["", "colour1", "colour2", "colour3"])
        new_colour_button = customtkinter.CTkButton(self, text="Add new colour... ")
        self.widget_grid.append([colour_lbl_str, colour_dropdown, new_colour_button])

        # type
        type_lbl_str = "Type:"
        type_dropdown = customtkinter.CTkOptionMenu(self, values = ["", "type1", "type2", "type3"])
        new_type_button = customtkinter.CTkButton(self, text="Add new type... ")
        self.widget_grid.append([type_lbl_str, type_dropdown, new_type_button])

        # subtype
        subtype_lbl_str = "Sub-Type:"
        subtype_dropdown = customtkinter.CTkOptionMenu(self, values = ["", "subtype1", "subtype2", "subtype3"])
        new_subtype_button = customtkinter.CTkButton(self, text="Add new subtype... ")
        self.widget_grid.append([subtype_lbl_str, subtype_dropdown, new_subtype_button])

        # stock
        stock_lbl_str = "Stock:"
        stock_spinbox = Spinbox(self)
        self.widget_grid.append([stock_lbl_str, stock_spinbox])

        # low stock
        low_stock_lbl_str = "Low Stock Warning:"
        low_stock_spinbox = Spinbox(self)
        self.widget_grid.append([low_stock_lbl_str, low_stock_spinbox])

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
            self.manage_component_window = ManageComponentWindow()
        else:
            self.manage_component_window.reappear()

class ManageComponentWindow(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Manage Components")

        # lock popup at front
        self.attributes("-topmost", "true")
        # make main window unclickable until popup is closed
        self.lock_at_front()

        # override the exit button as exiting produces an error, so we just
        # hide the window and restore it if necessary
        self.protocol("WM_DELETE_WINDOW", self.release_focus_and_hide)

        #CHANGE THIS - hard-coded examples
        component_data = [["Earring hook", 11],
                          ["Jump ring - large", 31],
                          ["Necklace chain", 4],
                          ["Earring back", 77],
                          ["Earring pouch", 27]]

        self.display_components(component_data)

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
