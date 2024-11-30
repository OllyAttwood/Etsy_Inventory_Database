import customtkinter
from db_tab_view import DBTabView

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        customtkinter.set_appearance_mode("dark")
        self.title("Product Database")

        # maximise window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}")

        # tab view
        self.tab_view = DBTabView(master=self)
        self.tab_view.grid(row=0, column=0, sticky="nesw")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

app = App()
app.mainloop()
