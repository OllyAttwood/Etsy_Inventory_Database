import customtkinter
from UI.view_items_frame import ViewItemsFrame
from UI.add_new_item_frame import AddNewItemFrame
from UI.low_stock_frame import LowStockFrame
from UI.splash import Splash

class DBTabView(customtkinter.CTkTabview):
    """The main view which controls which of the main frames is being displayed"""
    VIEW_ITEMS_FRAME_INDEX = 0
    ADD_NEW_ITEM_FRAME_INDEX = 1
    LOW_STOCK_FRAME_INDEX = 2
    TAB_NAMES = ("View Items", "Add New Item", "Low Stock")

    def __init__(self, master, presenter, **kwargs):
        super().__init__(master, border_width=3, **kwargs)

        self.presenter = presenter

        splash_screen = Splash(self, program_startup=True)

        for tab_name in DBTabView.TAB_NAMES:
            self.add(tab_name)

        # setup the different tab's frames
        self.view_items_frame = self.create_view_items_frame()
        self.add_new_item_frame = self.create_add_new_item_frame()
        self.low_stock_frame = self.create_low_stock_frame()
        self.tab_frames = [
            self.view_items_frame, self.add_new_item_frame, self.low_stock_frame
        ]

        for i, frame in enumerate(self.tab_frames):
            self.display_frame_in_grid(frame)
            #configure grid weights so that the frame covers the whole area
            self.tab(self.TAB_NAMES[i]).grid_rowconfigure(0, weight=1)
            self.tab(self.TAB_NAMES[i]).grid_columnconfigure(0, weight=1)

        splash_screen.destroy()

    def create_view_items_frame(self):
        return ViewItemsFrame(
            master=self.tab(self.TAB_NAMES[self.VIEW_ITEMS_FRAME_INDEX]),
            presenter=self.presenter,
            tab_view=self
        )

    def create_add_new_item_frame(self):
        return AddNewItemFrame(
            master=self.tab(self.TAB_NAMES[self.ADD_NEW_ITEM_FRAME_INDEX]),
            presenter=self.presenter,
            tab_view=self
        )

    def create_low_stock_frame(self):
        return LowStockFrame(
            master=self.tab(self.TAB_NAMES[self.LOW_STOCK_FRAME_INDEX]),
            presenter=self.presenter
        )

    def display_frame_in_grid(self, frame):
        """Displays the given frame"""
        frame.grid(row=0, column=0, sticky="nesw")

    def _reload_tab_contents(self, tab_num, replacement_frame):
        """Replaces the specified frame in this tab_view with a new one"""
        frame = self.tab_frames[tab_num]
        frame.destroy()
        self.display_frame_in_grid(replacement_frame)
        self.tab_frames[tab_num] = replacement_frame

    def _reload_view_items_frame(self, display_components):
        """
        Refreshes the ViewItemsFrame - display_components controls whether the
        components are initially displayed rather than the default products
        """
        replacement_frame = self.create_view_items_frame()
        self._reload_tab_contents(self.VIEW_ITEMS_FRAME_INDEX, replacement_frame)

        if display_components:
            replacement_frame.filter_bar.display_components()

    def _reload_add_new_item_frame(self):
        """Refreshes the AddNewItemFrame"""
        replacement_frame = self.create_add_new_item_frame()
        self._reload_tab_contents(self.ADD_NEW_ITEM_FRAME_INDEX, replacement_frame)

    def _reload_low_stock_frame(self):
        """Refreshes the LowStockFrame"""
        replacement_frame = self.create_low_stock_frame()
        self._reload_tab_contents(self.LOW_STOCK_FRAME_INDEX, replacement_frame)

    def reload_all_frames(self, display_components_in_view_items_frame=False):
        """
        Refreshes the UI with updated values. display_components_in_view_items_frame
        controls whether the components should be initially displayed in the
        ViewItemsFrame (e.g. immediately after updating the stock level of a component)
        """
        splash = Splash(self)

        self._reload_view_items_frame(display_components_in_view_items_frame)
        self._reload_add_new_item_frame()
        self._reload_low_stock_frame()

        splash.destroy()
