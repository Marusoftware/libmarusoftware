from . import WidgetBase

class Notebook(WidgetBase):
    def __init__(self, master, parent, command=None, close=None, onzero=None, **options):
        super().__init__(master)
        self.parent=parent
        if close is None:
            from tkinter.ttk import Notebook
            self.widget=Notebook(self.master, **options)
        else:
            from .widgets import CustomNotebook
            self.widget=CustomNotebook(self.master, **options)
        self.widget.enable_traversal()
        if close and not command is None:
            self.widget.bind("<<NotebookTabClosed>>",lambda null: command(self.value))
        self.value=None
        self.widget.bind("<<NotebookTabChanged>>", self.callback)
        self.onzero=onzero
    def add_tab(self, label="", **options):
        child=self.parent.Frame()
        self.widget.add(child=child.root, text=label, **options)
        return child
    def select_tab(self, tab):
        self.widget.select(self.tab2id(tab))
    def del_tab(self, tab):
        self.widget.forget(self.tab2id(tab))
    def config_tab(self, tab, **options):
        self.widget.tab(self.tab2id(tab), **options)
    def list_tab(self):
        return [self.widget.tab(i, "text") for i in self.widget.tabs()]
    def callback(self, *event):
        try:
            id=self.widget.index("current")
        except:
            if callable(self.onzero): self.onzero()
        else:
            self.value=self.widget.tab(id, "text")
    def tab2id(self, tab):
        if tab=="end":
            return self.widget.tabs()[-1]
        elif tab=="current":
            return self.widget.index("current")
        else:
            for id in self.widget.tabs():
                if tab == self.widget.tab(id, "text"):
                    break
            return id