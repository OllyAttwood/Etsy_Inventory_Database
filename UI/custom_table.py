import customtkinter
from tkinter import StringVar
import tkinter.font as tkfont

# class to create a table widget
class CustomTable(customtkinter.CTkFrame):
    def __init__(self, master, data, columns, font_size=15, header_colour="black",
                 data_colour="grey", cell_hover_colour="gray60",
                 selected_row_colour = "SteelBlue1"):
        super().__init__(master)

        self.master = master
        self.data = data
        self.columns = columns
        self.combined_data = [columns] + data
        self.column_widths = self.calculate_column_widths(self.combined_data, font_size)
        self.font = (None, font_size)
        self.cell_hover_colour = cell_hover_colour
        self.data_colour = data_colour
        self.selected_row_colour = selected_row_colour
        self.selected_row = None
        self.tooltip = None

        # verify data is correct
        self.check_is_data_correct_shape()

        # display table
        for row_num, row in enumerate(self.combined_data):
            for col_num, cell_text in enumerate(row):
                cell_width = self.column_widths[col_num]
                cell = customtkinter.CTkEntry(self, textvariable=StringVar(self, cell_text),
                                              font=self.font, state="disabled", fg_color=data_colour,
                                              width=cell_width)
                cell.grid(row=row_num, column=col_num)

                # header row
                if row_num == 0:
                    cell.configure(fg_color=header_colour)
                # data rows
                else:
                    # hover bindings
                    cell.bind("<Enter>", self.on_mouse_enter_cell)
                    cell.bind("<Leave>", self.on_mouse_leave_cell)
                    cell.bind("<Motion>", self.on_mouse_motion)
                    #click binding
                    cell.bind("<Button-1>", self.click_row)

    def check_is_data_correct_shape(self):
        if len(self.data) == 0:
            return

        num_cols_in_data = len(self.data[0])

        for row in self.data:
            if len(row) != num_cols_in_data:
                raise Exception("Rows in data are different lengths")

        if len(self.columns) != num_cols_in_data:
            raise Exception("Number of column names is different to data")

    def change_row_colour(self, row_num, grid_info, colour):
        cells_in_row = grid_info["in"].grid_slaves(row=row_num)

        for cell in cells_in_row:
            cell.configure(fg_color=colour)

    def click_row(self, event):
        # must use event.widget.master below instead of just event.widget
        # see https://stackoverflow.com/questions/75361805/customtkinter-why-does-this-event-widget-lose-the-proper-grid-information
        grid_info = event.widget.master.grid_info()
        row_num = grid_info["row"]

        if self.selected_row:
            self.change_row_colour(self.selected_row, grid_info, self.data_colour)

        self.selected_row = row_num
        self.change_row_colour(row_num, grid_info, self.selected_row_colour)
        print(row_num)

    def update_table_appearance(self, event, colour):
        # must use event.widget.master below instead of just event.widget
        # see https://stackoverflow.com/questions/75361805/customtkinter-why-does-this-event-widget-lose-the-proper-grid-information
        grid_info = event.widget.master.grid_info()
        row_num = grid_info["row"]

        if row_num != self.selected_row:
            self.change_row_colour(row_num, grid_info, colour)

    def on_mouse_enter_cell(self, event):
        self.update_table_appearance(event, self.cell_hover_colour)

    def on_mouse_leave_cell(self, event):
        self.update_table_appearance(event, self.data_colour)

        # remove tooltip
        if self.tooltip is not None:
            self.tooltip.destroy()
            self.tooltip = None

    def on_mouse_motion(self, event):
        # calculate tooltip position
        absolute_x = event.widget.winfo_rootx() + event.x # the position of it in the whole window
        absolute_y = event.widget.winfo_rooty() + event.y
        relative_x = absolute_x - self.master.winfo_rootx() # subtract the position of the CustomTable frame - needed for correct tooltip placement
        relative_y = absolute_y - self.master.winfo_rooty()

        self.show_tooltip(event.widget.get(), relative_x, relative_y)

    def show_tooltip(self, text, x, y):
        """Shows the tooltip for a CustomTable. The x and y values are for the master frame the CustomTable
        is contained within, as the tooltip will be placed on the frame rather than the CustomTable so that
        the tooltip is still displayed when its outside of the bounds of the CustomTable.
        """
        x_offset = 10
        y_offset = -25

        # create tooltip if deleted / not created yet
        if self.tooltip == None:
            self.tooltip = customtkinter.CTkLabel(self.master, text=text, padx=20)

        self.tooltip.place(x=x+x_offset, y=y+y_offset) # slightly adjust x and y so tooltip is not covered by cursor or cut off at bottom

    def calculate_column_widths(self, full_data, font_size, min_width=100, max_width=350):
        font = tkfont.Font(size=font_size)
        column_widths = [min_width] * len(full_data[0])

        for row in full_data:
            for column_num, cell_text in enumerate(row):
                width = font.measure(cell_text)

                if width > min_width and width < max_width and width > column_widths[column_num]:
                    column_widths[column_num] = width

        return column_widths
