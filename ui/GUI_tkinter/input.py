from . import WidgetBase
import os

class _Button(WidgetBase):
    def __init__(self, master, label, **options):
        super().__init__(master)
        from tkinter.ttk import Button
        if not "command" in options:
            from tkinter import IntVar
            self.var=IntVar(master=self.master, value=0)
            options["command"]=lambda: self.var.set(self.var.get()+1)
            self.widget=Button(self.master, text=label, **options)
        else:
            self.var=None
            self.widget=Button(self.master, text=label, **options)
    def wait(self):
        if self.var is None:
            return
        self.widget.wait_variable(self.var)
    def release(self):
        if self.var is None:
            return
        self.var.set(self.var.get()+1)
class _Form(WidgetBase):
    def __init__(self, master, parent, type="text", command=None, **options):
        from tkinter.ttk import Entry, Frame
        from tkinter import StringVar
        super().__init__(master, parent=parent)
        self.type=type
        self.var=StringVar(self.master)
        self.value=""
        self.var.trace("w",self.callback)
        self.command=[command]
        self.options=options
        if type=="password":
            options.update(show="●")
            self.widget=Entry(self.master, textvariable=self.var, **options)
        elif type=="text":
            self.widget=Entry(self.master, textvariable=self.var, **options)
        elif "file" in type:
            self.widget=parent.Frame()
            self.widget.setup_dnd(self.on_press, "file")
            self.widget.form=Entry(self.widget.root, textvariable=self.var)
            self.widget.form.pack(fill="x", side="left", expand=True)
            from tkinter.ttk import Button
            self.widget.button=Button(self.widget.root, text="Select...", command=self.on_press)
            self.widget.button.pack(side="right")
    def callback(self, *args):
        self.value=self.var.get()
        if callable(self.command[0]): self.command[0]()
    def on_press(self, event=None):
        if event is None:
            if "save" in self.type:
                file=self.parent.Dialog.askfile(save=True, **self.options)
            elif "open" in self.type:
                file=self.parent.Dialog.askfile(**self.options)
                if not os.path.exists(file):
                    return
            elif "openmulti" in self.type:
                file=self.parent.Dialog.askfile(multi=True, **self.options)
                if not os.path.exists(file):
                    return
            else:
                file=self.parent.Dialog.askfile(multi=True, **self.options)
                if not os.path.exists(file):
                    return
        else:
            file=event.data
        self.widget.form.delete(0,"end")
        self.widget.form.insert("end", file)
    def set(self, value):
        self.var.set(value)
class _Text(WidgetBase):
    def __init__(self, master, parent, scroll=True, command=None, readonly=False, **options):
        from tkinter import Text
        super().__init__(master, parent=parent)
        self.type=type
        if scroll:
            try:
                from tkinter.scrolledtext import ScrolledText as Text
            except:
                from .scrolledtext import ScrolledText as Text
        self.readonly=readonly
        self.widget=Text(self.master, state=("disabled" if self.readonly else "normal"),**options)
        if not command is None:
            self.widget.bind("<<Modified>>", lambda event: command())
    def insert(self, *args, **options):
        if self.readonly:
            self.configure(state="normal")
        self.widget.insert(*args, **options)
        if self.readonly:
            self.configure(state="disabled")
    def get(self, *args, **options):
        return self.widget.get(*args, **options)
    def delete(self, *args, **options):
        self.widget.delete(*args, **options)
    def undo(self):
        self.widget.edit_undo()
    def redo(self):
        self.widget.edit_redo()
class _List(WidgetBase):
    def __init__(self, master, columns=[], header=False, scroll=True, **options):
        super().__init__(master)
        from tkinter.ttk import Treeview
        show=["tree"]
        if header: show.append("headings")
        if scroll:
            from .widgets import ScrolledTreeview
            self.widget=ScrolledTreeview(self.master, show=show, columns=columns, **options)
        else:    
            self.widget=Treeview(self.master, show=show, columns=columns, **options)
        self.widget.bind("<<TreeviewSelect>>", self.callback)
        self.value=()
    def set_header(self, column, text):
        self.widget.heading(column, text=text)
    def add_item(self, parent="", index=0, id=None, label="", values=None, **options):
        if not id is None:
            options.update(iid=id)
        if not values is None:
            options.update(values=values)
        self.widget.insert(parent=parent, index=index, text=label, **options)
    def callback(self, event):
        self.value=self.widget.selection()
    def set_selection(self, items):
        self.value=items
        self.widget.selection_set(items)
    def exist_item(self, id):
        return self.widget.exists(id)
class _CheckButton(WidgetBase):
    def __init__(self, master, label=None, command=None, default=False, **options):
        super().__init__(master)
        from tkinter import BooleanVar
        from tkinter.ttk import Checkbutton
        self.var=BooleanVar(self.master, value=default)
        self.value=""
        self.var.trace("w",self.callback)
        self.command=[command]
        if not label is None:
            options.update(text=label)
        self.widget=Checkbutton(self.master, variable=self.var, **options)
    def callback(self, *args):
        self.value=self.var.get()
        if callable(self.command[0]): self.command[0]()
class _Select(WidgetBase):
    def __init__(self, master, default="", command=None, values=[], inline=False, label="", **options):
        super().__init__(master)
        from tkinter import StringVar
        from tkinter.ttk import Frame, Label
        self.var=StringVar(self.master, value=default)
        self.inline=inline
        self.value=default
        self.command=[command]
        self.values=values
        self.widget=Frame(self.master, **options)
        if label != "":
            self.label=Label(self.widget, text=label)
            self.label.pack(side="left")
        if inline:
            from tkinter.ttk import OptionMenu
            self.children=OptionMenu(master=self.widget, variable=self.var, command=self.callback, **options)
            self.children.set_menu(default, *values)
            self.children.pack(side="left", fill="x")
        else:
            self.children={}
            for value in values:
                self.add_item(value)
    def add_item(self, label=None, **options):
        if self.inline:
            self.values.append(label)
            self.children.set_menu(*self.children)
        else:
            from tkinter.ttk import Radiobutton
            if not label is None:
                options.update(text=label, value=label)
            self.children.append(Radiobutton(self.widget, variable=self.var, command=self.callback, **options))
            self.children[-1].pack(side="left", fill="x")
    def del_item(self, label):
        if self.inline:
            self.children.pop(label)
            self.widget.set_menu(*self.children)
        else:
            self.children[label].destroy()
    def callback(self, *args):
        self.value=self.var.get()
        self.command[0]()
class Input(WidgetBase):
    def Button(self, **options):
        return _Button(self.master, **options)
    def List(self, **options):
        return _List(self.master, **options)
    def Form(self, **options):
        return _Form(self.master, self.parent, **options)
    def Text(self, **options):
        return _Text(self.master, self.parent, **options)
    def CheckButton(self, **options):
        return _CheckButton(self.master, **options)
    def Select(self, **options):
        return _Select(self.master, **options)