from tkinter import *
from color_table import *
from itertools import cycle

rgb_iter = cycle(color_table)


def on_leave(e):
    bt.configure(fg=def_fg)


def on_enter(e):
    bt.configure(activeforeground=next(rgb_iter))
    bt.after(10, on_enter, e)


def do_nothing():
    pass


root = Tk()

bt = Button(root, text='да ладно это легко', font=('Helvetica', 15, 'bold'), command=do_nothing)
bt.pack()
def_fg = bt['fg']
bt.bind("<Enter>", on_enter)
bt.bind("<Leave>", on_leave)

root.mainloop()
