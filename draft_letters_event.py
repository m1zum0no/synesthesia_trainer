from tkinter import Button, Tk
from itertools import cycle
from spectral_glow import letters_fg_color_range
from operator import add, sub


def get_speed_list(start_speed, end_speed, length):
    diff = abs(end_speed - start_speed)
    func = add if start_speed < end_speed else sub
    return [func(start_speed, i // (length // diff)) for i in range(length)]


rgb_iter = cycle(letters_fg_color_range)
speed_iter = cycle(get_speed_list(5, 25, len(letters_fg_color_range)))


def on_leave(e):
    if hasattr(bt, 'after_ident'):
        bt.after_cancel(bt.after_ident)
    bt.configure(fg='black')


def on_enter(e):
    bt.configure(activeforeground=next(rgb_iter))
    bt.after_ident = bt.after(next(speed_iter), on_enter, e)


def do_nothing():
    pass


root = Tk()

dummy_bt = Button(root)
default_button_bg = dummy_bt['bg']

bt = Button(root, text='A', font=('Helvetica', 35, 'bold'), command=do_nothing,
            borderwidth=0,activebackground=default_button_bg, highlightbackground=default_button_bg,
            highlightthickness=0)
bt.pack()

bt.bind("<Enter>", on_enter)
bt.bind("<Leave>", on_leave)

root.mainloop()
