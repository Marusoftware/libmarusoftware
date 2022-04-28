# -*- coding: utf-8 -*-

try:
    import Tkinter as tkinter
    import Tix as tix
    import ttk
except ImportError:
    import tkinter
    from tkinter import tix
    from tkinter import ttk
import os, re, platform
TkdndVersion = None
# dnd actions
PRIVATE = 'private'
NONE = 'none'
ASK = 'ask'
COPY = 'copy'
MOVE = 'move'
LINK = 'link'
REFUSE_DROP = 'refuse_drop'
# dnd types
DND_TEXT = 'DND_Text'
DND_FILES = 'DND_Files'
DND_ALL = '*'
CF_UNICODETEXT = 'CF_UNICODETEXT'
CF_TEXT = 'CF_TEXT'
CF_HDROP = 'CF_HDROP'
FileGroupDescriptor = 'FileGroupDescriptor - FileContents'# ??
FileGroupDescriptorW = 'FileGroupDescriptorW - FileContents'# ??

def _require(tkroot):
    '''Internal function.'''
    global TkdndVersion
    tkdndlib = os.environ.get('TKDND_LIBRARY')
    if tkdndlib != "__null__":
        if tkdndlib:
            tkroot.tk.eval('global auto_path; lappend auto_path {%s}' % tkdndlib)
    try:
        TkdndVersion = tkroot.tk.call('package', 'require', 'tkdnd')
    except tkinter.TclError:
        raise RuntimeError('Unable to load tkdnd library.')
    return TkdndVersion

class DnDEvent:
    pass

class DnDWrapper:
    _subst_format_dnd = ('%A', '%a', '%b', '%C', '%c', '{%CST}',
                         '{%CTT}', '%D', '%e', '{%L}', '{%m}', '{%ST}',
                         '%T', '{%t}', '{%TT}', '%W', '%X', '%Y')
    _subst_format_str_dnd = " ".join(_subst_format_dnd)
    tkinter.BaseWidget._subst_format_dnd = _subst_format_dnd
    tkinter.BaseWidget._subst_format_str_dnd = _subst_format_str_dnd

    def _substitute_dnd(self, *args):
        if len(args) != len(self._subst_format_dnd):
            return args
        def getint_event(s):
            try:
                return int(s)
            except ValueError:
                return s
        def splitlist_event(s):
            try:
                return self.tk.splitlist(s)
            except ValueError:
                return s

        A, a, b, C, c, CST, CTT, D, e, L, m, ST, T, t, TT, W, X, Y = args
        ev = DnDEvent()
        ev.action = A
        ev.actions = splitlist_event(a)
        ev.button = getint_event(b)
        ev.code = C
        ev.codes = splitlist_event(c)
        ev.commonsourcetypes = splitlist_event(CST)
        ev.commontargettypes = splitlist_event(CTT)
        ev.data=[]
        state=""
        for i in D:
            if state=="{":
                if i == "}":
                    state=""
                else:
                    ev.data[-1]+=i
            elif i=="{":
                state="{"
                if len(ev.data) != 0:
                    if ev.data[-1]=="":
                        continue
                ev.data.append("")
            else:
                if i == " ":
                    ev.data.append("")
                else:
                    if len(ev.data)==0:
                        ev.data.append("")
                    ev.data[-1]+=i
        ev.name = e
        ev.types = splitlist_event(L)
        ev.modifiers = splitlist_event(m)
        ev.supportedsourcetypes = splitlist_event(ST)
        ev.sourcetypes = splitlist_event(t)
        ev.type = T
        ev.supportedtargettypes = splitlist_event(TT)
        try:
            ev.widget = self.nametowidget(W)
        except KeyError:
            ev.widget = W
        ev.x_root = getint_event(X)
        ev.y_root = getint_event(Y)
        return (ev,)
    tkinter.BaseWidget._substitute_dnd = _substitute_dnd

    def _dnd_bind(self, what, sequence, func, add, needcleanup=True):
        if isinstance(func, str):
            self.tk.call(what + (sequence, func))
        elif func:
            funcid = self._register(func, self._substitute_dnd, needcleanup)
            # FIXME: why doesn't the "return 'break'" mechanism work here??
            #cmd = ('%sif {"[%s %s]" == "break"} break\n' % (add and '+' or '',
            #                              funcid, self._subst_format_str_dnd))
            cmd = '%s%s %s' %(add and '+' or '', funcid,
                                    self._subst_format_str_dnd)
            self.tk.call(what + (sequence, cmd))
            return funcid
        elif sequence:
            return self.tk.call(what + (sequence,))
        else:
            return self.tk.splitlist(self.tk.call(what))
    tkinter.BaseWidget._dnd_bind = _dnd_bind

    def dnd_bind(self, sequence=None, func=None, add=None):
        return self._dnd_bind(('bind', self._w), sequence, func, add)
    tkinter.BaseWidget.dnd_bind = dnd_bind

    def drag_source_register(self, button=None, *dndtypes):
        if button is None:
            button = 1
        else:
            try:
                button = int(button)
            except ValueError:
                # no button defined, button is actually
                # something like DND_TEXT
                dndtypes = (button,) + dndtypes
                button = 1
        self.tk.call(
                'tkdnd::drag_source', 'register', self._w, dndtypes, button)
    tkinter.BaseWidget.drag_source_register = drag_source_register

    def drag_source_unregister(self):
        self.tk.call('tkdnd::drag_source', 'unregister', self._w)
    tkinter.BaseWidget.drag_source_unregister = drag_source_unregister

    def drop_target_register(self, *dndtypes):
        self.tk.call('tkdnd::drop_target', 'register', self._w, dndtypes)
    tkinter.BaseWidget.drop_target_register = drop_target_register

    def drop_target_unregister(self):
        self.tk.call('tkdnd::drop_target', 'unregister', self._w)
    tkinter.BaseWidget.drop_target_unregister = drop_target_unregister

    def platform_independent_types(self, *dndtypes):
        return self.tk.split(self.tk.call(
                            'tkdnd::platform_independent_types', dndtypes))
    tkinter.BaseWidget.platform_independent_types = platform_independent_types

    def platform_specific_types(self, *dndtypes):
        return self.tk.split(self.tk.call(
                            'tkdnd::platform_specific_types', dndtypes))
    tkinter.BaseWidget.platform_specific_types = platform_specific_types

    def get_dropfile_tempdir(self):
        return self.tk.call('tkdnd::GetDropFileTempDirectory')
    tkinter.BaseWidget.get_dropfile_tempdir = get_dropfile_tempdir

    def set_dropfile_tempdir(self, tempdir):
        self.tk.call('tkdnd::SetDropFileTempDirectory', tempdir)
    tkinter.BaseWidget.set_dropfile_tempdir = set_dropfile_tempdir

class Tk(tkinter.Tk, DnDWrapper):
    def __init__(self, *args, **kw):
        tkinter.Tk.__init__(self, *args, **kw)
        self.TkdndVersion = _require(self)

class TixTk(tix.Tk, DnDWrapper):
    def __init__(self, *args, **kw):
        tix.Tk.__init__(self, *args, **kw)
        self.TkdndVersion = _require(self)
