try:
    import Tkinter as tk
    import ttk
except ImportError:  # Python 3
    import tkinter as tk
    from tkinter import ttk

class CustomNotebook(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab
    This code was copied from https://stackoverflow.com/questions/39458337/is-there-a-way-to-add-close-buttons-to-tabs-in-tkinter-ttk-notebook"""

    __initialized = False

    def __init__(self, master, *args, **kwargs):
        self.master=master
        if not self.__initialized:
            self.__initialize_custom_style()
            self.__inititialized = True

        kwargs["style"] = "WithClose.TNotebook"
        ttk.Notebook.__init__(self, master, *args, **kwargs)
        self._active = None

        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""

        element = self.identify(event.x, event.y)

        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(['pressed'])
            self._active = index

    def on_close_release(self, event):
        """Called when the button is released over the close button"""
        if not self.instate(['pressed']):
            return

        element =  self.identify(event.x, event.y)
        index = self.index("@%d,%d" % (event.x, event.y))

        if "close" in element and self._active == index:
            #self.forget(index)
            self.event_generate("<<NotebookTabClosed>>")

        self.state(["!pressed"])
        self._active = None

    def __initialize_custom_style(self):
        style = ttk.Style(master=self.master)
        self.style=style
        if not "WithClose.TNotebook.close" in style.element_names():
            self.images = (
                tk.PhotoImage("img_close", master=self.master, data='''
                    R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                    d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                    5kEJADs=
                    '''),
                tk.PhotoImage("img_closeactive", master=self.master, data='''
                    R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                    AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                    '''),
                tk.PhotoImage("img_closepressed", master=self.master, data='''
                    R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                    d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                    5kEJADs=
                ''')
            )

            style.element_create("WithClose.TNotebook.close", "image", "img_close",
                                ("active", "pressed", "!disabled", "img_closepressed"),
                                ("active", "!disabled", "img_closeactive"), border=8, sticky='')
        style.layout("WithClose.TNotebook", [("WithClose.TNotebook.client", {"sticky": "nswe"})])
        style.layout("WithClose.TNotebook.Tab", [
            ("WithClose.TNotebook.tab", {
                "sticky": "nswe", 
                "children": [
                    ("WithClose.TNotebook.padding", {
                        "side": "top", 
                        "sticky": "nswe",
                        "children": [
                            ("WithClose.TNotebook.focus", {
                                "side": "top", 
                                "sticky": "nswe",
                                "children": [
                                    ("WithClose.TNotebook.label", {"side": "left", "sticky": ''}),
                                    ("WithClose.TNotebook.close", {"side": "left", "sticky": ''}),
                                ]
                            })
                        ]
                    })
                ]
            })   
        ])

from tkinter import Frame, Pack, Grid, Place
from tkinter.ttk import Treeview, Scrollbar
from tkinter.constants import HORIZONTAL, NSEW

class ScrolledTreeview(Treeview):
    """
    This code was copied from https://cercopes-z.com/Python/stdlib-tkinter-widget-treeview-py.html#ex-scrollbar
    """
    def __init__(self, master=None, **kw):
        name = kw.get("name")
        if name == None:
            name = ""
        self.frame = Frame(master, name=name)
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.vbar = Scrollbar(self.frame)
        self.vbar.grid(row=0, column=1, sticky="NWS")
        self.hbar = Scrollbar(self.frame, orient=HORIZONTAL)
        self.hbar.grid(row=1, column=0, sticky="SWE")

        kw.update({'yscrollcommand': self.vbar.set})
        kw.update({'xscrollcommand': self.hbar.set})
        Treeview.__init__(self, self.frame, **kw)
        self.grid(row=0, column=0, sticky=NSEW)
        self.vbar['command'] = self.yview
        self.hbar['command'] = self.xview

        text_meths = vars(Treeview).keys()
        methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        methods = methods.difference(text_meths)
        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))

    def forget_hbar(self):
        self.hbar.grid_forget()

    def forget_vbar(self):
        self.vbar.grid_forget()

    def __str__(self):
        return str(self.frame)