from . import WidgetBase

class Label(WidgetBase):
    def __init__(self, master, label=None, **options):
        super().__init__(master=master)
        from tkinter.ttk import Label
        self.widget=Label(self.master, text=label, wraplength=master.winfo_width() ,**options)
        self.master.bind("<Configure>", self.update_width)
        self.width=0
    def update_width(self, event):
        if self.width!=event.width:
            self.width=event.width
            self.widget.configure(wraplength=self.width)
    def configure(self, **options):
        if "label" in options:
            options["text"]=options["label"]
            options.pop("label")
        super().configure(**options)

class Image(WidgetBase):#TODO: resize, configure
    def __init__(self, master, image=None, **options):
        super().__init__(master=master)
        if not image is None:
            from PIL import Image, ImageTk
            self.image=ImageTk.PhotoImage(Image.open(image), master=self.master)
            options.update(image=self.image)
        from tkinter.ttk import Label
        self.widget=Label(self.master, **options)