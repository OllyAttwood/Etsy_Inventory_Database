import customtkinter
from view_items_frame import ViewItemsFrame
from add_new_item_frame import AddNewItemFrame
from low_stock_frame import LowStockFrame

class DBTabView(customtkinter.CTkTabview):
    tab_names = ("View Items", "Add New Item", "Low Stock")

    def __init__(self, master, **kwargs):
        super().__init__(master, border_width=3, **kwargs)

        for tab_name in DBTabView.tab_names:
            self.add(tab_name)

        # setup the different tab's frames
        self.view_items_frame = ViewItemsFrame(master=self.tab(self.tab_names[0]))
        self.add_new_item_frame = AddNewItemFrame(master=self.tab(self.tab_names[1]))
        self.low_stock_frame = LowStockFrame(master=self.tab(self.tab_names[2]))

        for i, frame in enumerate([self.view_items_frame, self.add_new_item_frame,
                                   self.low_stock_frame]):
            frame.grid(row=0, column=0, sticky="nesw")
            self.tab(self.tab_names[i]).grid_rowconfigure(0, weight=1)
            self.tab(self.tab_names[i]).grid_columnconfigure(0, weight=1)
