__all__=["GUI", "TUI", "WEB", "UI"]

def UI(config, logger):
    return GUI(config, logger)

def GUI(config, logger, library="auto"):
    from .GUI_tkinter import TKINTER
    return TKINTER(config, logger)

def TUI():
    pass

def WEB():
    pass