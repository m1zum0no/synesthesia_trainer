from tkinter import Button, Tk
from itertools import cycle
from color_gradient_with_options import *

rgb_iter = cycle(colormap_hex)


def on_leave(e):
    if hasattr(bt, 'after_ident'):
        bt.after_cancel(bt.after_ident)
    bt.configure(fg=def_fg)


def on_enter(e):
    bt.configure(activeforeground=next(rgb_iter))
    bt.after_ident = bt.after(speed_arg, on_enter, e)


def do_nothing():
    pass


root = Tk()

bt = Button(root, text='■', font=('Helvetica', 15, 'bold'), command=do_nothing)
bt.pack()

def_fg = bt['fg']
bt.bind("<Enter>", on_enter)
bt.bind("<Leave>", on_leave)

root.mainloop()
