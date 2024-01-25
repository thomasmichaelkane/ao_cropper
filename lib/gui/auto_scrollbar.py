import tkinter as tk
from tkinter import ttk

class AutoScrollbar(ttk.Scrollbar):
    """
    A subclass of ttk.Scrollbar that automatically hides itself when it's not needed.
    
    Only the grid geometry manager should be used with this widget. The pack and place 
    geometry managers are disabled and will raise a tk.TclError if used.
    """

    def set(self, lo, hi):

        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
            ttk.Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
 
        raise tk.TclError("Cannot use pack with this widget.")

    def place(self, **kw):

        raise tk.TclError("Cannot use place with this widget.")
