"""The file to run to start the program"""
from UI.app import App
from presenter import Presenter

if __name__ == "__main__":
    presenter = Presenter()
    app = App(presenter)
    app.mainloop()
