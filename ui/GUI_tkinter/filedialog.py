import platform
import tkinter.filedialog as fd
custom=False
if platform.system() == "Linux":
    try:
        import tkfilebrowser as fd
    except:
        custom=False
    else:
        custom=True

#dialogs
def askdirectory(title="Open...", initialdir=None, **argv):
    if not initialdir is None:
        argv["initialdir"]=initialdir
    if custom:
        return fd.askopendirname(title=title, **argv)
    else:
        return fd.askdirectory(title=title, **argv)

def askopenfilename(**argv):
    if platform.system() == "Darwin":
        import tkfilebrowser as fd2
        return fd2.askopenfilename(**argv)
    if custom:
        return fd.askopenfilename(**argv)
    else:
        return fd.askopenfilename(**argv)

def askopenfilenames(fd=None, **argv):
    if platform.system() == "Darwin":
        import tkfilebrowser as fd2
        return fd2.askopenfilenames(**argv)
    if custom:
        return fd.askopenfilenames(**argv)
    else:
        return fd.askopenfilenames(**argv)

def asksaveasfilename(**argv):
    if custom:
        return fd.asksaveasfilename(**argv)
    else:
        return fd.asksaveasfilename(**argv) 