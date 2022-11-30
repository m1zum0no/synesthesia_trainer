# السلام عليكم
from tkinter import filedialog, PhotoImage, Menu, Tk, Frame, Text, Scrollbar, Label, Button, StringVar, OptionMenu
from tkinter.constants import END, WORD, X, TOP, RIGHT, Y, E, BOTTOM, W, SEL, INSERT
import arabic_reshaper
from tkinter import messagebox
from bidi.algorithm import get_display

diff_lvl = ['e', 't', 'a', 'o', 'i', 'n',
            's', 'r', 'h', 'l', 'd', 'c', 
            'u', 'm', 'f', 'p', 'g', 'w', 
            'y', 'b', 'v', 'k', 'x', 'j',
            'q', 'z', 'ﺍ']

color_table = {'def': '#ffffff', 'e': '#8accd2', 't': '#d2908a', 'a': '#d1c78a', 'o': '#8a94d1',
               'i': '#b98ad1', 'n': '#a2d18a', 's': '#d5ff0a', 'r': '#b7efe0',
               'h': '#596f69', 'l': '#171136', 'd': '#423e56', 'c': '#b989be',
               'u': '#21236d', 'm': '#426a4a', 'f': '#ddc96c', 'p': '#b3b3af',
               'g': '#77afa1', 'w': '#4c70ac', 'y': '#53ac4c', 'b': '#86ac4c',
               'v': '#395213', 'k': '#758162', 'x': '#619a0b', 'j': '#35755a',
               'q': '#b6e037', 'z': '#622c2d', 'ﺍ': '#FF0000'}

def rgb(hex_rgb):
    str_rgb = hex_rgb.replace('#', '')
    r = int(str_rgb[:2], 16)
    g = int(str_rgb[2:4], 16)
    b = int(str_rgb[4:], 16)
    return f'\033[38;2;{r};{g};{b}m'


def encode_color(ch):
    if ch.lower() in diff_lvl:
        return rgb(color_table[ch.lower()]) + ch
    return ch

def apply_color():  # palette preview
    text_str = textbox.get(1.0, END)
    global is_colored
    if not is_colored and not (len(text_str) == 0 or text_str.isspace()):
        if 'def_color' in textbox.tag_names():
            textbox.tag_remove('def_color', 1.0, END)
        lines = text_str.splitlines(True)
        for line_index, line in enumerate(lines, start=1):
            for char_index, ch in enumerate(line):
                if ch.lower() in diff_lvl:
                    color = color_table[ch.lower()]
                    textbox.tag_add(color, f'{line_index}.{char_index}')
            for color in color_table.values():
                textbox.tag_config(color, foreground=color)
            is_colored = True
    else:
        def_color = 'black'
        textbox.tag_add('def_color', 1.0, END)
        textbox.tag_config('def_color', foreground=def_color)
        is_colored = False

# root frame
root = Tk()
root.title('Synesthesia Trainer')
root.geometry('800x570')

# toolbar frame
toolbar_frame = Frame(root)
toolbar_frame.pack(fill=X, side=TOP)

# textbox frame
text_frame = Frame(root, width=800, height=570)
text_frame.grid_propagate(False)
text_frame.pack(fill="both", expand=True)
text_frame.grid_rowconfigure(0, weight=1)
text_frame.grid_columnconfigure(0, weight=1)

textbox = Text(text_frame,
               width=76, height=20, selectbackground='grey', selectforeground='white',
               wrap=WORD)
textbox.grid(row=0, column=0, sticky="nsew")

def set_text_string(text):
    textbox.delete(1.0,"end")  # tracking down the coursor 
    textbox.insert(1.0, text)

def rearrange_arabic_to_rtl():
    text_to_be_reshaped = textbox.get(1.0, END)  # one line & set coursor ptr
    reshaped_text = arabic_reshaper.reshape(text_to_be_reshaped)
    bidi_text = get_display(reshaped_text)
    set_text_string(bidi_text)

# for toggling on-off state
global is_colored
is_colored = False
apply_palette_button = Button(toolbar_frame, text='apply color', command=apply_color, borderwidth=0,
                            highlightthickness=0)
apply_palette_button.grid(row=0, column=5)


Arabic = Button(root, 
                   height=1, 
                   width=10, 
                   text="Reshape", 
                   command=lambda:rearrange_arabic_to_rtl())
Arabic.pack()

root.mainloop()