import os
from libtools.exception import UIError
from libtools.ui.GUI_tkinter.menu import Menu as _Menu

class TKINTER():
    def __init__(self, config, logger, type="main", parent=None, label=None, **options):
        self.parent=parent
        self.logger=logger
        self.config=config
        self.type=type
        self.appinfo=config.appinfo
        self.backend="tkinter"
        self.children=[]
        self.icons=[]
        if type=="main":
            try:
                import tkinter
            except:
                raise UIError("GUI is not supported")
            os.environ['TKDND_LIBRARY'] = os.path.join(self.appinfo["share_os"],"tkdnd")
            try:
                from .tkdnd import Tk
                self._root=Tk(className=self.appinfo["appname"])
            except Exception as e:
                self.logger.exception(e)
                from tkinter import Tk
                self._root=Tk(className=self.appinfo["appname"])
                self.dnd = False
            else:
                self.dnd = True
            self._root.report_callback_exception=self.tkerror
            self.changeTitle(self.appinfo["appname"])
            #gttk
            try:
                from gttk import GTTK
                self._root.gtk=GTTK(self._root)
                from tkinter.ttk import Style
            except:
                self.logger.info("GTK is disabled.")
                self.logger.exception("gttk: ")
                self._root.gtk=None
            else:
                self.logger.info("GTK is enabled.")
            #ttkthemes
            try:
                from ttkthemes import ThemedStyle as Style
                self._root.style = Style(master=self._root)
            except:
                from tkinter.ttk import Style
                self._root.style = Style(master=self._root)
            if not self._changeTheme(self.config["theme"]):
                if self._root.style.theme_use() != "gttk":
                    self.config["theme"]=self._root.style.theme_use()
                else:
                    self.config["theme"]=self._root.gtk.get_current_theme()
                self.logger.info("Theme is not found. So, use default.")
            self.style=self._root.style
        elif type=="frame":
            self.dnd=self.parent.dnd
            from tkinter.ttk import Frame, Labelframe
            if label is None:
                self._root=Frame(self.parent.root, **options)
            else:
                self._root=Labelframe(self.parent.root, text=label, **options)
        else:
            from tkinter import Toplevel
            self._root=Toplevel(master=self.parent._root)
            self.dnd=self.parent.dnd
            if type=="dialog":
                self._root.wait_visibility()
                self._root.focus_set()
                self._root.grab_set()
                self.parent._root.attributes("-topmost", False)
        self.aqua=(self.appinfo["os"] == "Darwin" and self._root.tk.call('tk', 'windowingsystem') == "aqua")
        if type!="frame":
            import tkinter.ttk as ttk
            self.root=ttk.Frame(self._root)
            self.root.pack(fill="both", expand=True)
        else:
            self.root=self._root
        from .dialog import Dialog
        self.Dialog=Dialog(self._root)
        from .input import Input
        self.Input=Input(self.root, parent=self)
    def _changeTheme(self, theme=None):
        if theme is None: return False
        if theme in self._root.style.theme_names():
            self._root.style.theme_use(theme)
        elif not self._root.gtk is None:
            if theme in self._root.gtk.get_themes_available():
                self._root.style.theme_use("gttk")
                self._root.gtk.set_gtk_theme(theme)
            else:
                return False
        else:
            return False
        self.logger.info("Theme:"+theme)
        return True
    def changeTitle(self, title):
        self._root.title(title)
    def changeIcon(self, icon_path):
        from PIL import Image, ImageTk
        icon=ImageTk.PhotoImage(Image.open(icon_path), master=self._root)
        self._root.iconphoto(True, icon)
        self.icons.append(icon)
    def fullscreen(self, tf=None):
        if tf is None:
            tf = not self._root.attributes("-fullscreen")
        self._root.attributes("-fullscreen", tf)
    def tkerror(self, *args):
        import tkinter, traceback
        err = traceback.format_exception(*args)
        self.logger.error("tkinter: "+"\n".join(err))
        sorry = tkinter.Toplevel()
        sorry.title("Marueditor - Error")
        tkinter.Label(sorry,text="We're sorry.\n\nError is happen.").pack()
        t = tkinter.Text(sorry)
        t.pack()
        t.insert("end","Error report=========\n")
        t.insert("end",str("\n".join(err))+"\n")
        t.configure(state="disabled")
        tkinter.Button(sorry, text="EXIT", command=sorry.destroy).pack()
        sorry.focus_set()
        sorry.grab_set()
    def changeSize(self, size):
        self._root.geometry(size)
    def uisetting(self, frame, txt):
        themes=list(self._root.style.theme_names())
        if "gttk" in themes:
            themes.remove("gttk")
        if not self._root.gtk is None:
            themes.extend(self._root.gtk.get_themes_available())
        theme=frame.Input.Select(values=themes, inline=True, default=self.config["theme"], command=lambda: (self._changeTheme(theme.value),self.config.update(theme=theme.value)), label=txt["style"]+":")
        theme.pack(fill="x")
    def setcallback(self, name, callback):
        if name=="close":
            self._root.protocol("WM_DELETE_WINDOW", callback)
            if self.aqua:
                self._root.createcommand('tk::mac::Quit', callback)
        elif name=="macos_help" and self.aqua:
            self._root.createcommand('tk::mac::ShowHelp', callback)
        elif name=="macos_settings" and self.aqua:
            self._root.createcommand('tk::mac::ShowPreferences')
    def Menu(self, type, **options):
        return _Menu(self._root, type=type, **options)
    def Notebook(self, close=None, command=None, **options):
        from .note import Notebook
        child=Notebook(self.root, self, command=command, close=close, **options)
        self.children.append(child)
        return child
    def makeSubWindow(self, dialog=False, **options):
        child=TKINTER(self.config, self.logger, type=("dialog" if dialog else "sub"), parent=self, **options)
        self.children.append(child)
        return child
    def Frame(self, **options):
        child=_Frame(logger=self.logger, parent=self, config=self.config, **options)
        self.children.append(child)
        return child
    def Label(self, label="", **options):
        from .base import Label
        return Label(self.root, label=label, **options)
    def Image(self, image=None, **options):
        from .base import Image
        if not image is None:
            if "/" in image:
                return
            options.update(image=os.path.join(self.appinfo["image"],image))
        return Image(self.root, **options)
    def close(self):
        self._root.destroy()
    def wait(self):
        self._root.wait_window()
    def mainloop(self):
        self._root.mainloop()
    def exist(self):
        return self._root.winfo_exists()

class WidgetBase():
    def __init__(self, master, **options):
        self.backend="tkinter"
        self.master=master
        self.placer=None
        if "parent" in options:
            self.parent=options["parent"]
    def pack(self, **options):
        self.widget.pack(**options)
        self.placer="pack"
    def grid(self, **options):
        self.widget.grid(**options)
        self.placer="grid"
    def place(self, **options):
        self.widget.place(**options)
        self.placer="place"
    def hide(self, **options):
        if self.placer is None:
            pass
        elif "pack":
            self.widget.pack_forget(**options)
        elif "grid":
            self.widget.pack_forget(**options)
        elif "place":
            self.widget.pack_forget(**options)
    def configure(self, **options):
        self.widget.configure(**options)
    def destroy(self):
        self.widget.destroy()
    def exist(self):
        return self.widget.winfo_exists()

class _Frame(TKINTER):
    def __init__(self, logger, parent, config, label=None, **options):
        super().__init__(logger=logger, config=config, type="frame", parent=parent, label=label)
        self.widget=self.root
        self.master=self.parent.root
        self.placer=None
    def pack(self, **options):
        self.widget.pack(**options)
        self.placer="pack"
    def grid(self, **options):
        self.widget.grid(**options)
        self.placer="grid"
    def place(self, **options):
        self.widget.place(**options)
        self.placer="place"
    def hide(self, **options):
        if self.placer is None:
            pass
        elif "pack":
            self.widget.pack_forget(**options)
        elif "grid":
            self.widget.pack_forget(**options)
        elif "place":
            self.widget.pack_forget(**options)
    def configure(self, **options):
        self.widget.configure(**options)
    def destroy(self):
        self.widget.destroy()
    def configure(self, **options):
        self.widget.configure(**options)
    def destroy(self):
        self.widget.destroy()
    def setup_dnd(self, command, target):
        if self.dnd:
            from .tkdnd import DND_ALL, DND_FILES, DND_TEXT
            if target=="file":
                target=DND_FILES
            elif target=="text":
                target=DND_TEXT
            else:
                target=DND_ALL
            self.root.drop_target_register(target)
            self.root.dnd_bind('<<Drop>>', command)
        