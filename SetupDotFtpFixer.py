from tkinter import Tk
from tkinter.filedialog import askdirectory
import os
import shutil

def ModifySetupFile(filename):
    if len(filename) == 0:
        return

    if "setup.ftp" not in filename:
        print("ModifySetupFile: bad file supplied: "+filename)
        return

    # Save the old setup.ftp as a backup, but only the first time through
    backupname=filename+".backup"
    if not os.path.exists(backupname):
        shutil.copyfile(filename, backupname)

    # Open and read setup.ftp
    fd=open(filename, "r")
    lines=fd.readlines()

    # The first line is the one to be changed.
    if len(lines) < 1:
        print("ModifySetupFile: empty file found: "+filename)
        return

    # The line should look like this:
    #    fanac.org; fanac.org; *; /public/[thing]/[name]
    # and should change it to
    #    fanac.org; fan@fanac.org; *; /[thing]/[name]
    # where [name] is the fanzine name and [thing] is the name of a category of pub (e.g., "worldcon" or "fanzine"

    print("\n"+lines[0].strip())
    chunks=lines[0].split("; ")
    if len(chunks) != 4:
        print("ModifySetupFile: couldn't find four chunks in: "+lines[0])
        return
    chunks[1]="fan@"+chunks[1].strip()
    chunks[3]=chunks[3].strip()
    if not chunks[3].startswith("/public"):
        print("ModifySetupFile: chunk 4 does not begin with '/public' in: "+lines[0])
        return
    chunks[3]=chunks[3][7:]
    line="; ".join(chunks)
    lines[0]=line

    print(lines[0])

def WalkDirectory(dirname):
    if len(dirname) == 0:
        return
    if not os.path.isdir(dirname):
        return

    # First deal with any setup.ftp file present
    setup=os.path.join(dirname, "setup.ftp")
    if os.path.exists(setup):
        ModifySetupFile(setup)

    # Now walk any subdirectories
    subdirs=os.listdir(dirname)
    subdirs=[os.path.join(dirname, d) for d in subdirs if os.path.isdir(os.path.join(dirname, d))]  # Remove list elements that are not directory names
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

