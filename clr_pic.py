import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor
#import prog
#from prog import *

root = tk.Tk()
root.title('Tkinter Color Chooser')
root.geometry('300x150')

def change_color():
    clr = askcolor(title="Tkinter Color Chooser")[1]  #hex code of the color

ttk.Button(root, text='Выбрать цвет', command=change_color).pack(expand=True)

root.mainloop()