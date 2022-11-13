from tkinter import *
from tkinter import filedialog
from tkinter import font
from PIL import Image, ImageTk  # sudo apt-get install python3-pil.imagetk

diff_lvl = [ 'e', 't', 'a', 'o', 'i','n', 
            's', 'r', 'h', 'l', 'd', 'c', 
            'u', 'm', 'f', 'p', 'g', 'w', 
'y', 'b', 'v', 'k', 'x', 'j', 'q', 'z'  ]

color_table = {'def': '#ffffff','e': '#8accd2', 't': '#d2908a', 'a': '#d1c78a', 'o': '#8a94d1', 
'i': '#b98ad1', 'n': '#a2d18a', 's': '#d5ff0a', 'r': '#b7efe0', 
'h': '#596f69', 'l': '#171136', 'd': '#423e56', 'c': '#b989be', 
'u': '#21236d', 'm': '#426a4a', 'f': '#ddc96c', 'p': '#b3b3af', 
'g': '#77afa1', 'w': '#4c70ac', 'y': '#53ac4c', 'b': '#86ac4c', 
'v': '#395213', 'k': '#758162', 'x': '#619a0b', 'j': '#35755a', 
'q': '#b6e037', 'z': '#622c2d'}

# for OS-dependent icon rendition
def find_platform():
    import sys
    if sys.platform.startswith('linux'):
        return 'Linux'
    elif sys.platform == 'darwin':
        return 'Mac'
    elif ('win' in sys.platform and not 'dar') or 'msys':
        return 'Win'

def display_window_icon():
    if platform_name == 'Linux':
        #try:
        icon = Image.open(r'./icons/text-editor.xbm')
        icon = icon.resize((32, 32), Image.ANTIALIAS)
        root.call('wm', 'iconphoto', root._w, icon)
        #except:
        #    pass
    else:
        icon = Image.open(r'./icons/text-editor.png')
        try:  # for Mac
            root.iconbitmap(icon) 
        except:  # Windows
            if icon.mode in ['RGBA', 'P']:  # for testing other icon options:
                # remove format attributes that hinder further conversion     
                icon = icon.convert('RGB')
            icon.save('./icons/text-editor.ico', format = 'ICO', sizes=[(32,32)])
            # makes icon default for all the window descendents
            root.iconbitmap(default='./icons/text-editor.ico')

# adding standard functionality Ctrl-A
def select_all(press_key_event):
    textbox.tag_add('sel', '1.0', 'end')

def text_to_bold():
    bold_font = font.Font(textbox, textbox.cget("font"))
    bold_font.configure(weight='bold')
    # tag configuration
    textbox.tag_configure('bold', font=bold_font)
    set_tags = textbox.tag_names('sel.first')
    # toggle on-off 
    if 'bold' in set_tags:
        textbox.tag_remove('bold', 'sel.first', 'sel.last')
    else:
        textbox.tag_add('bold', 'sel.first', 'sel.last')

def text_to_italics():
    italics_font = font.Font(textbox, textbox.cget("font"))
    italics_font.configure(slant='italic')
    # tag configuration
    textbox.tag_configure('italic', font=italics_font)
    set_tags = textbox.tag_names('sel.first')
    # toggle on-off  
    if 'italic' in set_tags:
        textbox.tag_remove('italic', 'sel.first', 'sel.last')
    else:
        textbox.tag_add('italic', 'sel.first', 'sel.last')

def rgb(hex_rgb):
    str_rgb = hex_rgb.replace('#', '')
    r = int(str_rgb[:2], 16)
    g = int(str_rgb[2:4], 16)
    b = int(str_rgb[4:], 16)
    return f'\033[38;2;{r};{g};{b}m'

def encode_color(ch):
    if ch.lower() in diff_lvl[:5 * 5]:
        return rgb(color_table[ch.lower()]) + ch
    return ch

# display names of the currently opened files
def update_status(filepath):
    try:
        last_slash = filepath.rindex('/', 0, -1)  # exclude last posiible '\' in the end of the file path
        filename = filepath[last_slash::].replace('/', '')
    except ValueError:
        filename = filepath.replace('/', '')
    root.title(f'{filename} - Synesthesia Trainer')
    status_bar.config(text=f'{filename}   ')

def save_file_as():
    output_file = filedialog.asksaveasfilename(defaultextension='.*', title='Введите название...')
    if output_file:  # if not 'cancel'
        update_status(output_file)
        with open(output_file, 'w', encoding='utf-8') as output_file:
            txt = textbox.get(1.0, END)
            for ch in txt:
                output_file.write(encode_color(ch)) 

def load_file():
    # prep for loading
    clear  # rm prev contents
    input_file = filedialog.askopenfilename(title='Выберите файл...')
    input_file = input_file.replace('\\', '/')
    update_status(input_file)
    # load the file
    with open(input_file, 'r', encoding='utf-8') as input_file:
        loaded_text = input_file.read()
        textbox.insert(END, loaded_text)

# buttons
def clear():
    textbox.delete(1.0, END)
    root.title('Synesthesia Trainer')
    status_bar.config(text='')

def apply_color():  # editing of text by char
    text_str = textbox.get(1.0, END)
    lines = text_str.splitlines(True)
    for line_index, line in enumerate(lines, start=1):
        for char_index, ch in enumerate(line):
            if ch.lower() in diff_lvl[:5 * 5]:
                color = color_table[ch.lower()]
                textbox.tag_add(color, f'{line_index}.{char_index}')
    for color in color_table.values():
        textbox.tag_config(color, foreground=color)

# root frame
root = Tk()
root.title('Synesthesia Trainer')
root.geometry('800x570')
global platform_name
platform_name = find_platform()

# test necessity of making changes for WinOS
if platform_name == 'Windows':
    # enable ansi escape characters in terminal 
    import os
    os.system("")  # stands for "color"
    """ 
    # alternative
    import os
    from ctypes import windll
    k = windll.kernel32
    k.SetConsoleMode(k.GetStdHandle(-11), 7)
    """

display_window_icon()

# toolbar frame
toolbar_frame = Frame(root)
toolbar_frame.pack(fill=X, side=TOP)

# textbox frame
text_frame = Frame(root, width=800, height=570)
text_frame.grid_propagate(False)
text_frame.pack(fill="both", expand=True)
text_frame.grid_rowconfigure(0, weight=1)
text_frame.grid_columnconfigure(0, weight=1)

scroll_frame = Frame(text_frame)
scroll_frame.grid(sticky="nw")

# scrollbar init
scroll_output = Scrollbar(scroll_frame, orient='vertical')
scroll_output.pack(side=RIGHT, fill=Y)

# text widget
textbox = Text(text_frame, width=76, height=20, selectbackground='grey', selectforeground='white', wrap=WORD, yscrollcommand=scroll_output.set)
textbox.grid(row=0, column=0, sticky="nsew")

# scrollbar config
scroll_output.config(command=textbox.yview)

# configuring key shortcut
root.bind('<Control-A>', select_all)


# toolbar buttons
img_bold = ImageTk.PhotoImage((Image.open('./icons/b.png')).resize((47,47)))
bold_button = Button(toolbar_frame, image=img_bold, command=text_to_bold, borderwidth=0)
bold_button.grid(row=0, column=0, sticky=W, pady=2)

img_italics = ImageTk.PhotoImage((Image.open('./icons/i.png')).resize((41,41)))
italics_button = Button(toolbar_frame, image=img_italics, command=text_to_italics, borderwidth=0)
italics_button.grid(row=0, column=1, pady=8)

select_all_button = Button(toolbar_frame, text='Выделить все', command=lambda: select_all(True))
select_all_button.grid(row=0, column=2)

clear_button = Button(toolbar_frame, text='Очистить', command=clear)
clear_button.grid(row=0, column=3, padx=10)

img_color = ImageTk.PhotoImage((Image.open('./icons/color-palette.png')).resize((35,35)))
apply_button = Button(toolbar_frame, image=img_color, command=apply_color, borderwidth=0)
apply_button.grid(row=0, column=4)


# Menu
top_menu = Menu(root)
root.config(menu=top_menu)

# Menu options
menu_option_file = Menu(top_menu, tearoff=False)
top_menu.add_cascade(label='Файл', menu=menu_option_file)

menu_option_file.add_command(label='Открыть', command=load_file)
menu_option_file.add_command(label='Создать')
menu_option_file.add_command(label='Сохранить как...', command=save_file_as)
menu_option_file.add_separator()
menu_option_file.add_command(label='Выйти', command=root.quit)

menu_option_palette = Menu(top_menu, tearoff=False)
top_menu.add_cascade(label='Палитра', menu=menu_option_palette)
menu_option_palette.add_command(label='Настроить')
menu_option_palette.add_command(label='Выбрать')

menu_option_level = Menu(top_menu, tearoff=False)
top_menu.add_cascade(label='Уровень', menu=menu_option_level)
menu_option_level.add_command(label='Описание')
menu_option_level.add_command(label='Выбрать')

# Status bar
status_bar = Label(root, text='', anchor=E)
status_bar.pack(fill=X, side=BOTTOM, pady=5)  


root.mainloop()