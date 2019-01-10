from tkinter import Tk
from tkinter.filedialog import askdirectory
import os

def WalkDirectory(dirname):
    print("Walking "+dirname)
    if len(dirname) == 0:
        return
    if not os.path.isdir(dirname):
        return

    # First deal with any setup.ftp file present
    setup=os.path.join(dirname, "setup.ftp")
    if os.path.exists(setup):
        print(setup)

    # Now walk any subdirectories
    subdirs=os.listdir(dirname)
    subdirs=[os.path.join(dirname, d) for d in subdirs if os.path.isdir(os.path.join(dirname, d))]
    for subdir in subdirs:
        WalkDirectory(subdir)


# Ask for the root directory
root = Tk()
root.filename =  askdirectory(initialdir = ".",title = "Choose the Root Directory")
dirname=root.filename
root.withdraw()

if len(dirname) == 0:
    exit(0)

# Recursively walk the root directory looking for and fixing setup.ftp files.
WalkDirectory(dirname)

