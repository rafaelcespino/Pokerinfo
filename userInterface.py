import tkinter as tk
from automateSpreadsheet import main as automain
from functools import partial

window = tk.Tk()
window.title("Spreadsheet Updater")
URL = tk.Entry(window)
URL.pack()

def printURL():
    automain(URL.get())

submit = tk.Button(window, text="Submit", command=printURL)
submit.pack()



window.mainloop() 

