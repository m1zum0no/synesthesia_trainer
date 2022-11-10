from tkinter import *
from tkinter import font

def change_font(press_key_event):
    set_font.config(
        family=font_listbox.get(font_listbox.curselection())
    )

def change_font_size(press_key_event):
    set_font.config(
        size=font_size_listbox.get(font_size_listbox.curselection())
    )
# root frame
root = Tk()
root.title('Synesthesia Trainer')
root.geometry('800x570')
"""try:
    root.iconbitmap('./path_to_icon')
except"""

set_font = font.Font(family='Helvetica', size='16')

# main frame that everything holds onto 
main_frame = Frame(root, width=500, height=250)
main_frame.pack(pady=5)
# freezing the size of the main frame
main_frame.grid_propagate(False)
main_frame.grid_columnconfigure(0, weight=10)

# ensuring textbox doesn't change size dynamically dependend on font size
textbox = Text(main_frame, font=set_font, width=76, height=20, selectbackground='grey', selectforeground='white', wrap=WORD)
textbox.grid(row=0, column=0)
textbox.grid_rowconfigure(0, weight=1)
textbox.grid_columnconfigure(0, weight=1)

# listbox frame
font_frame = Frame(root)
font_frame.pack()

#inscription labels
font_label = Label(font_frame, text='Font') 
font_label.grid(row=0, column=0)

size_label = Label(font_frame, text='Size')
size_label.grid(row=0, column=1)

# Font listbox
font_listbox = Listbox(font_frame, selectmode=SINGLE, width=40)
font_listbox.grid(row=1, column=0)

# Size listbox
font_size_listbox = Listbox(font_frame, selectmode=SINGLE, width=20)
font_size_listbox.grid(row=1, column=1)

# add fonts to listbox
for f in font.families():
    font_listbox.insert(END, f)

# add sizes to listbox
font_sizes = [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36]
for s in font_sizes:
    font_size_listbox.insert(END, s)

# bind font listbox and font changing function
font_listbox.bind('<ButtonRelease-1>', change_font)
font_size_listbox.bind('<ButtonRelease-1>', change_font_size)

root.mainloop()
