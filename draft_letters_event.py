from tkinter import Button, Tk
from itertools import cycle
from spectral_glow import letters_fg_color_range

rgb_iter = cycle(letters_fg_color_range)


def on_leave(e):
    if hasattr(bt, 'after_ident'):
        bt.after_cancel(bt.after_ident)
    bt.configure(fg=def_fg)


def on_enter(e):
    bt.configure(activeforeground=next(rgb_iter))
    bt.after_ident = bt.after(15, on_enter, e)


def do_nothing():
    pass


root = Tk()

dummy_bt = Button(root)
default_button_color = dummy_bt['bg']
bt = Button(root, text='A', font=('Helvetica', 20, 'bold'), command=do_nothing,
            borderwidth=0,activebackground=default_button_color, highlightbackground=default_button_color,
            highlightthickness=0)
bt.pack()

def_fg = bt['fg']
bt.bind("<Enter>", on_enter)
bt.bind("<Leave>", on_leave)

root.mainloop()
