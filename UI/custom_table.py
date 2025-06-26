import customtkinter
from tkinter import StringVar
import tkinter.font as tkfont

# class to create a table widget
class CustomTable(customtkinter.CTkFrame):
    def __init__(self, master, data, columns, font_size=15, header_colour="black",
                 data_colour="grey", cell_hover_colour="gray60",
                 selected_row_colour = "SteelBlue1"):
        super().__init__(master)

        self.data = data
        self.columns = columns
        self.combined_data = [columns] + data
        self.column_widths = self.calculate_column_widths(self.combined_data, font_size)
        self.font = (None, font_size)
        self.cell_hover_colour = cell_hover_colour
        self.data_colour = data_colour
        self.selected_row_colour = selected_row_colour
        self.selected_row = None

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
                    cell.bind("<Enter>", lambda event: self.mouse_hover_data_cell(event, cell_hover_colour))
                    cell.bind("<Leave>", lambda event: self.mouse_hover_data_cell(event, data_colour))
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

    def mouse_hover_data_cell(self, event, colour):
        # must use event.widget.master below instead of just event.widget
        # see https://stackoverflow.com/questions/75361805/customtkinter-why-does-this-event-widget-lose-the-proper-grid-information
        grid_info = event.widget.master.grid_info()
        row_num = grid_info["row"]

        if row_num != self.selected_row:
            self.change_row_colour(row_num, grid_info, colour)

    def calculate_column_widths(self, full_data, font_size, min_width=100, max_width=350):
        font = tkfont.Font(size=font_size)
        column_widths = [min_width] * len(full_data[0])

        for row in full_data:
            for column_num, cell_text in enumerate(row):
                width = font.measure(cell_text)

                if width > min_width and width < max_width and width > column_widths[column_num]:
                    column_widths[column_num] = width

        return column_widths
