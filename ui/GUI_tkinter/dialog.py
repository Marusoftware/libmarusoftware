from . import WidgetBase

class Dialog(WidgetBase):
    def askfile(self, multi=False, save=False, **options):
        from .filedialog import askopenfilename, askopenfilenames, asksaveasfilename
        if save:
            return asksaveasfilename(parent=self.master, **options)
        else:
            if multi:
                return askopenfilenames(parent=self.master, **options)
            else:
                return askopenfilename(parent=self.master, **options)
    def askdir(self, **options):
        from .filedialog import askdirectory
        return askdirectory(parent=self.master, **options)
    def error(self, **options):
        from tkinter.messagebox import showerror
        return showerror(parent=self.master, **options)
    def info(self, **options):
        from tkinter.messagebox import showinfo
        return showinfo(parent=self.master, **options)
    def warn(self, **options):
        from tkinter.messagebox import showwarning
        return showwarning(parent=self.master, **options)
    def question(self, type, title, message, **options):
        from tkinter.messagebox import askokcancel, askretrycancel, askyesno, askyesnocancel
        if type=="okcancel":
            return askokcancel(parent=self.master, title=title, message=message, **options)
        elif type=="retrycancel":
            return askretrycancel(parent=self.master, title=title, message=message, **options)
        elif type=="yesno":
            return askyesno(parent=self.master, title=title, message=message, **options)
        elif type=="yesnocancel":
            return askyesnocancel(parent=self.master, title=title, message=message, **options)
        elif type=="text":
            from tkinter.simpledialog import askstring
            return askstring(parent=self.master, title=title, prompt=message, **options)