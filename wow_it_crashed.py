from tkinter import *
from tkinter import font
from tkinter.constants import SINGLE, END, WORD, BROWSE
from tkinter.ttk import Treeview, Style


def change_font(event):
    set_font.config(family=font_treeview.item(font_treeview.selection()[0]).get('text'))
    #font_treeview.item('Main', text=set_font['family'])
    button.config(text=set_font['family'])

def display_font_picker():
    style = Style()
    global font_treeview
    font_treeview = Treeview(popup, show='tree', selectmode=BROWSE)
    font_treeview.grid(row=1, column=0)
    font_treeview.column('#0', width=250)
    for font_name in fonts:
        font_tag = font_name.replace(' ', '_')
        font_treeview.insert('', END, text=font_name, tags=(font_tag,))
        font_treeview.tag_configure(font_tag, font=(font_name, 11))
        font_treeview.tag_bind(font_tag, '<ButtonRelease-1>', change_font)
        # adjusting sizes of the cells by font height
        font_height = font.Font(font=font_tag).metrics('ascent')*1.3 + font.Font(font=font_tag).metrics('descent')*2
        style.configure('Treeview', rowheight=int(font_height))
    # removing some empty row from a treeview 
    font_treeview.delete(font_treeview.get_children()[81])
    font_treeview.bind('<<TreeviewSelect>>', change_font)

def click():
    global popup
    popup = Toplevel(root)
    popup.title('Шрифт')
    display_font_picker()

# root frame
root = Tk()
root.title('Synesthesia Trainer')
root.geometry('800x570')

set_font = font.Font(family='Helvetica', size=16)

# main frame that everything holds onto 
main_frame = Frame(root, width=500, height=250)
main_frame.pack(pady=5)
# freezing the size of the main frame
main_frame.grid_propagate(False)
main_frame.grid_columnconfigure(0, weight=10)

# listbox frame
treeview_frame = Frame(root, width=76, height=20)
treeview_frame.pack(expand=False)

button_frame = Frame(root)
button_frame.pack()
button = Button(root, text=set_font['family'], command=click)
button.pack()

# add fonts to treeview
fonts = sorted(set(font.families()))
# remove Noto Color Emoji, which causes the app to crash for some unknown reason
if 'Noto Color Emoji' in fonts:
    fonts.remove('Noto Color Emoji')

root.mainloop()