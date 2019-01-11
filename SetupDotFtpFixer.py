from tkinter import Tk
from tkinter.filedialog import askdirectory
import os
import shutil

#-----------------------------
def ModifySetupFile(filename, log):
    if len(filename) == 0:
        return

    if "setup.ftp" not in filename:
        log.write("ModifySetupFile: wrong file supplied: "+filename+"\n")
        return

    # Save the old setup.ftp as a backup, but only the first time through
    backupname=filename+".backup"
    if not os.path.exists(backupname):
        shutil.copyfile(filename, backupname)

    # Open and read setup.ftp
    fd=open(filename, "r")
    lines=fd.readlines()
    fd.close()

    # The first line is the one to be changed.
    if len(lines) < 1:
        log.write("ModifySetupFile: empty file found: "+filename+"\n")
        return

    # The line should look like this:
    #    fanac.org; fanac.org; *; /public/[thing]/[name]
    # and should change it to
    #    fanac.org; fan@fanac.org; *; /[thing]/[name]
    # where [name] is the fanzine name and [thing] is the name of a category of pub (e.g., "worldcon" or "fanzine"

    log.write(lines[0].strip()+"\n")
    chunks=lines[0].split("; ")
    if len(chunks) != 4:
        log.write("ModifySetupFile: couldn't find four chunks in: "+lines[0]+"\n")
        return

    # If this file has already been processed, the 'fan@' will already be prepended to chunk #1 -- skip it.
    if chunks[1].startswith("fan@"):
        log.write("ModifySetupFile: file already processed\n")
        return

    chunks[1]="fan@"+chunks[1].strip()  # Prepend the 'fan@'

    # Remove the leading '/public'
    chunks[3]=chunks[3].strip()
    if not chunks[3].startswith("/public"):
        log.write("ModifySetupFile: chunk 4 does not begin with '/public' in: "+lines[0]+"\n")
        return
    chunks[3]=chunks[3][7:]

    # Reassemble the chunks and replace the first line with the modified first line
    line="; ".join(chunks)+"\n"
    lines[0]=line

    log.write(lines[0]+"\n")

    # For now, write the updated file as ".new"
    fd=open(filename+".new", "w")
    fd.writelines(lines)
    fd.close()

    return


#---------------------------------------------------------------
# If there's a setup.fpt file in the director, process it.
# Then call WalkDirectory on all the subdirectories of this directory.
def WalkDirectory(dirname, log):
    if len(dirname) == 0:
        return
    if not os.path.isdir(dirname):
        return

    # First deal with any setup.ftp file present
    setup=os.path.join(dirname, "setup.ftp")
    if os.path.exists(setup):
        ModifySetupFile(setup, log)

    # Now walk any subdirectories
    subdirs=os.listdir(dirname)
    subdirs=[os.path.join(dirname, d) for d in subdirs if os.path.isdir(os.path.join(dirname, d))]  # Remove list elements that are not directory names
    for subdir in subdirs:
        WalkDirectory(subdir, log)

    return


#---------------------------------------------------------------
# Main
# Ask for the root directory
root = Tk()
root.filename =  askdirectory(initialdir = ".",title = "Choose the Root Directory")
dirname=root.filename
root.withdraw()

if len(dirname) == 0:
    exit(0)


# Create the log file
log=open("SetupDotFtpFixerLog.txt", "w")

# Recursively walk the root directory looking for and fixing setup.ftp files.
WalkDirectory(dirname, log)

