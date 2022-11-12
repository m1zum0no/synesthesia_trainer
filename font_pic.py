from tkinter import font, Tk, Frame, Text, Label, Listbox, Scrollbar
from tkinter.constants import SINGLE, END, WORD, BROWSE
from tkinter.ttk import Treeview, Style


def change_font(event):
    set_font.config(
        family=font_treeview.item(font_treeview.selection()[0]).get('text')
    )


def change_font_size(press_key_event):
    set_font.config(
        size=font_size_listbox.get(font_size_listbox.curselection())
    )


# root frame
root = Tk()
root.title('Synesthesia Trainer')
root.geometry('800x570')
# try:
#     root.iconbitmap('./path_to_icon')
# except

set_font = font.Font(family='Helvetica', size=16)

# main frame that everything holds onto 
main_frame = Frame(root, width=500, height=250)
main_frame.pack(pady=5)
# freezing the size of the main frame
main_frame.grid_propagate(False)
main_frame.grid_columnconfigure(0, weight=10)

# ensuring textbox doesn't change size dynamically depending on font size
textbox = Text(main_frame,
               font=set_font, width=76, height=20, selectbackground='grey',
               selectforeground='white', wrap=WORD)
textbox.grid(row=0, column=0)
textbox.grid_rowconfigure(0, weight=1)
textbox.grid_columnconfigure(0, weight=1)

# listbox frame
font_frame = Frame(root)
font_frame.pack()

# inscription labels
font_label = Label(font_frame, text='Font') 
font_label.grid(row=0, column=0)

size_label = Label(font_frame, text='Size')
size_label.grid(row=0, column=1)

# Font listbox
font_treeview = Treeview(font_frame, show='tree', selectmode=BROWSE)
font_treeview.grid(row=1, column=0)
style = Style()
style.configure('Treeview', rowheight=27)

fonts_scrollbar = Scrollbar(font_frame, orient="vertical", command=font_treeview.yview)
fonts_scrollbar.grid(row=1, column=0, sticky='nse')
font_treeview.configure(yscroll=fonts_scrollbar.set, xscroll=fonts_scrollbar.set)

# Size listbox
font_size_listbox = Listbox(font_frame, selectmode=SINGLE, width=20)
font_size_listbox.grid(row=1, column=1)

# add fonts to listbox
for font_name in sorted(set(font.families())):
    font_tag = font_name.replace(' ', '_')
    font_treeview.insert('', END, text=font_name, tags=(font_tag,))
    font_treeview.tag_configure(font_tag, font=(font_name,))
    font_treeview.tag_bind(font_tag, '<ButtonRelease-1>', change_font)

# add sizes to listbox
font_sizes = [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36]
for s in font_sizes:
    font_size_listbox.insert(END, s)

# bind font listbox and font changing function
font_treeview.bind('<<TreeviewSelect>>', change_font)
font_size_listbox.bind('<ButtonRelease-1>', change_font_size)

root.mainloop()
