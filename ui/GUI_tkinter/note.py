from . import WidgetBase

class Tab:
    id=0
    frame=None
    def __init__(self, notebook):
        self._notebook=notebook
    @property
    def label(self):
        return self._notebook.tab(self.id, "text")
    @label.setter
    def label(self, value):
        self._notebook.tab(self.id, text=value)

class Notebook(WidgetBase):
    def __init__(self, master, parent, command=None, close=None, **options):
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
        self.tabs=[]
    def add_tab(self, label="", **options):
        tab=Tab(self.widget)
        tab.frame=self.parent.Frame()
        self.tabs.append(tab)
        self.widget.add(child=tab.frame.root, **options)
        tab.id=str(tab.frame.root)
        tab.label=label
        return tab
    def select_tab(self, tab):
        if isinstance(tab, Tab):
            self.widget.select(tab.id)
        else:
            self.widget.select(tab)
    def del_tab(self, tab):
        if isinstance(tab, Tab):
            self.widget.forget(tab.id)
            self.tabs.remove(tab)
        else:
            id=self.widget.tabs()[self.widget.index(tab)]
            for tab in self.tabs:
                if tab.id == id:
                    self.tabs.remove(tab)
                    break
    def config_tab(self, tab, **options):
        if isinstance(tab, Tab):
            return self.widget.tab(tab.id, **options)
        else:
            return self.widget.tab(tab, **options)
    def list_tab(self):
        return self.tabs
    def callback(self, *event):
        try:
            id=self.widget.tabs()[self.widget.index("current")]
        except:
            import traceback
            traceback.print_exc()
        else:
            for tab in self.tabs:
                if tab.id==id:
                    self.value=tab
                    break