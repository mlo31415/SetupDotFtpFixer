from tkinter import Tk
from tkinter.filedialog import askdirectory

root = Tk()
root.filename =  askdirectory(initialdir = ".",title = "Choose the Root Directory")
print (root.filename)
root.withdraw()