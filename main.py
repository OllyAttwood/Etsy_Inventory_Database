"""The file to run to start the program"""
from UI.app import App
from presenter import Presenter

presenter = Presenter()
app = App(presenter)
app.mainloop()
