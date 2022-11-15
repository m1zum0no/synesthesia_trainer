from tkinter import *
from itertools import cycle


rgb8 = ['#000040', '#000080', '#0000c0', '#002000', '#002040', '#002080', '#0020c0', '#004000', '#004040', '#004080', '#0040c0', '#006000', '#006040', '#006080', '#0060c0', '#008000', '#008040', '#008080', '#0080c0', '#00a000', '#00a040', '#00a080', '#00a0c0', '#00c400', '#00c440', '#00c480', '#00c4c0', '#00e000', '#00e040', '#00e080', '#00e0c0', '#200000', '#200040', '#200080', '#2000c0', '#202000', '#202040', '#202080', '#2020c0', '#204000', '#204040', '#204080', '#2040c0', '#206000', '#206040', '#206080', '#2060c0', '#208000', '#208040', '#208080', '#2080c0', '#20a000', '#20a040', '#20a080', '#20a0c0', '#20c400', '#20c440', '#20c480', '#20c4c0', '#20e000', '#20e040', '#20e080', '#20e0c0', '#400000', '#400040', '#400080', '#4000c0', '#402000', '#402040', '#402080', '#4020c0', '#404000', '#404040', '#404080', '#4040c0', '#406000', '#406040', '#406080', '#4060c0', '#408000', '#408040', '#408080', '#4080c0', '#40a000', '#40a040', '#40a080', '#40a0c0', '#40c400', '#40c440', '#40c480', '#40c4c0', '#40e000', '#40e040', '#40e080', '#40e0c0', '#600000', '#600040', '#600080', '#6000c0', '#602000', '#602040', '#602080', '#6020c0', '#604000', '#604040', '#604080', '#6040c0', '#606000', '#606040', '#606080', '#6060c0', '#608000', '#608040', '#608080', '#6080c0', '#60a000', '#60a040', '#60a080', '#60a0c0', '#60c400', '#60c440', '#60c480', '#60c4c0', '#60e000', '#60e040', '#60e080', '#60e0c0', '#800000', '#800040', '#800080', '#8000c0', '#802000', '#802040', '#802080', '#8020c0', '#804000', '#804040', '#804080', '#8040c0', '#806000', '#806040', '#806080', '#8060c0', '#808000', '#808040', '#808080', '#8080c0', '#80a000', '#80a040', '#80a080', '#80a0c0', '#80c400', '#80c440', '#80c480', '#80c4c0', '#80e000', '#80e040', '#80e080', '#80e0c0', '#a00000', '#a00040', '#a00080', '#a000c0', '#a02000', '#a02040', '#a02080', '#a020c0', '#a04000', '#a04040', '#a04080', '#a040c0', '#a06000', '#a06040', '#a06080', '#a060c0', '#a08000', '#a08040', '#a08080', '#a080c0', '#a0a000', '#a0a040', '#a0a080', '#a0a0c0', '#a0c400', '#a0c440', '#a0c480', '#a0c4c0', '#a0e000', '#a0e040', '#a0e080', '#a0e0c0', '#c40000', '#c40040', '#c40080', '#c400c0', '#c42000', '#c42040', '#c42080', '#c420c0', '#c44000', '#c44040', '#c44080', '#c440c0', '#c46000', '#c46040', '#c46080', '#c460c0', '#c48000', '#c48040', '#c48080', '#c480c0', '#c4a000', '#c4a040', '#c4a080', '#c4a0c0', '#c4c400', '#c4c440', '#c4c480', '#c4c4c0', '#c4e000', '#c4e040', '#c4e080', '#c4e0c0', '#e00000', '#e00040', '#e00080', '#e000c0', '#e02000', '#e02040', '#e02080', '#e020c0', '#e04000', '#e04040', '#e04080', '#e040c0', '#e06000', '#e06040', '#e06080', '#e060c0', '#e08000', '#e08040', '#e08080', '#e080c0', '#e0a000', '#e0a040', '#e0a080', '#e0a0c0', '#e0c400', '#e0c440', '#e0c480', '#e0c4c0', '#e0e000', '#e0e040', '#e0e080', '#e0e0c0']
rgb_iter = cycle(rgb8)


def on_leave(e):
    bt.configure(bg=def_bg)


def on_enter(e):
    bt.configure(activebackground=next(rgb_iter))
    bt.after(500, on_enter, e)


def do_nothing():
    pass


root = Tk()

bt = Button(root, command=do_nothing)
bt.pack()
def_bg = bt['bg']
next_index = 0 
bt.bind("<Enter>", on_enter)
bt.bind("<Leave>", on_leave)

root.mainloop()

'''
#Binding hovers
def on_start_hover():
    #What you do when the mouse hovers

def on_end_hover():
    #What to do when the mouse stops hovering

elem.bind('<Enter>', on_start_hover)
elem.bind('<Leave>', on_end_hover)
'''
