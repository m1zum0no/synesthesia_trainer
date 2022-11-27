import signal
from tkinter import filedialog, PhotoImage, Menu, Tk, Frame, Text, Scrollbar, Label, Button, StringVar, OptionMenu
from tkinter import font
from tkinter import ttk
from PIL import Image, ImageTk  # sudo apt-get install python3-pil.imagetk
from tkinter.constants import END, WORD, X, TOP, RIGHT, Y, E, BOTTOM, W, SEL, INSERT
from tktooltip import ToolTip  # pip install tkinter-tooltip
from popup import Popup
import polyglot   # pip install -U pycld2
from polyglot.detect import Detector 
from polyglot.detect.base import *

def detect_language():
    text = textbox.get("1.0", 'end-1c')
    try:
        tooltip_language_button.msg = Detector(text).languages[0].name
    except UnknownLanguage:
        pass
        #language_button.config(text="Language not detected")


diff_lvl = ['e', 't', 'a', 'o', 'i', 'n',
            's', 'r', 'h', 'l', 'd', 'c', 
            'u', 'm', 'f', 'p', 'g', 'w', 
            'y', 'b', 'v', 'k', 'x', 'j',
            'q', 'z']

color_table = {'def': '#ffffff', 'e': '#8accd2', 't': '#d2908a', 'a': '#d1c78a', 'o': '#8a94d1',
               'i': '#b98ad1', 'n': '#a2d18a', 's': '#d5ff0a', 'r': '#b7efe0',
               'h': '#596f69', 'l': '#171136', 'd': '#423e56', 'c': '#b989be',
               'u': '#21236d', 'm': '#426a4a', 'f': '#ddc96c', 'p': '#b3b3af',
               'g': '#77afa1', 'w': '#4c70ac', 'y': '#53ac4c', 'b': '#86ac4c',
               'v': '#395213', 'k': '#758162', 'x': '#619a0b', 'j': '#35755a',
               'q': '#b6e037', 'z': '#622c2d'}


def get_fonts():
    # retrieve all system fonts
    fonts = sorted(set(font.families()))
    # remove Noto Color Emoji font, which causes crashes on some systems
    if 'Noto Color Emoji' in fonts:
        fonts.remove('Noto Color Emoji')
    return fonts


def on_font_inserted(tw, item_id, tag):
    font_name = tw.item(item_id)['text']
    tw.tag_configure(tag, font=(font_name, 11))


def clear_font_box_highlight():
    current = font_size.get()
    font_size.set("")
    font_size.set(current)


def apply_font_size_change(event):
    set_font.config(size=font_size_menu.get())
    clear_font_box_highlight()


def apply_font_change(font_name):
    set_font.config(family=font_name)
    font_picker_opener.config(text=font_name)


def click_opener():
    font_popup.deiconify()


# for OS-dependent icon rendition
def find_platform():
    import sys
    if sys.platform.startswith('linux'):
        return 'Linux'
    elif sys.platform == 'darwin':
        return 'Mac'
    elif 'win' in sys.platform or sys.platform.startswith('msys'):
        return 'Win'


def display_window_icon():
    if platform_name == 'Linux':
        icon = PhotoImage(file='icons/icon.png')
        root.wm_iconphoto(True, icon)
#   icon = Image.open('icons/palette.png')        
#   if platform_name == 'Mac':
#       icon.save('icons/palette.icns',format = 'ICNS', sizes=[(32,32)])
#       root.iconbitmap('icons/palette.icns') 
    else:
        icon = Image.open('icons/palette.png')
        icon.save('./icons/palette.ico', format='ICO', sizes=[(32, 32)])
        root.iconbitmap('./icons/palette.ico')


def text_to_bold():
    # toggle on-off
    if set_font['weight'] == 'bold':
        set_font.config(weight='normal')
    else:
        set_font.config(weight='bold')


def text_to_italics():
    # toggle on-off
    if set_font['slant'] == 'italic':
        set_font.config(slant='roman')
    else:
        set_font.config(slant='italic')


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
    # rm prev contents
    close_file()
    input_file = filedialog.askopenfilename(title='Выберите файл...')
    input_file = input_file.replace('\\', '/')
    update_status(input_file)
    # load the file
    with open(input_file, 'r', encoding='utf-8') as input_file:
        loaded_text = input_file.read()
        textbox.insert(END, loaded_text)


# buttons
def close_file():
    textbox.delete(1.0, END)
    root.title('Synesthesia Trainer')
    status_bar.config(text='')


def apply_color():  # palette preview
    global is_colored
    if not is_colored:
        if 'def_color' in textbox.tag_names():
            textbox.tag_remove('def_color', 1.0, END)
        text_str = textbox.get(1.0, END)
        lines = text_str.splitlines(True)
        for line_index, line in enumerate(lines, start=1):
            for char_index, ch in enumerate(line):
                if ch.lower() in diff_lvl[:5 * 5]:
                    color = color_table[ch.lower()]
                    textbox.tag_add(color, f'{line_index}.{char_index}')
            for color in color_table.values():
                textbox.tag_config(color, foreground=color)
            tooltip_apply_palette.msg = 'Отменить палитру'
            is_colored = True
    else:
        def_color = 'black'
        textbox.tag_add('def_color', 1.0, END)
        textbox.tag_config('def_color', foreground=def_color)
        tooltip_apply_palette.msg = 'Применить палитру'
        is_colored = False

# adding standard functionality Ctrl-A
def select_all(press_key_event):
    textbox.tag_add(SEL, '1.0', END)
    return 'break'


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

# Text widget and its scrollbar 
scroll_output = Scrollbar(scroll_frame, orient='vertical')
scroll_output.pack(side=RIGHT, fill=Y)
set_font = font.Font(family='Helvetica', size=16)
textbox = Text(text_frame, font=set_font,
               width=76, height=20, selectbackground='grey', selectforeground='white',
               wrap=WORD, yscrollcommand=scroll_output.set)
textbox.grid(row=0, column=0, sticky="nsew")
textbox.bind("<Control-Key-a>", select_all)
textbox.bind("<Control-Key-A>", select_all)
scroll_output.config(command=textbox.yview)

# Toolbar buttons
# Font Picker setup 

font_picker_opener = Button(toolbar_frame, text=set_font['family'], font='TkDefaultFont', height=1, command=click_opener, relief='sunken')
popup_opened = False  # flag for tracking multiple attempts to open popups
font_picker_opener.grid(row=0, column=2)

img_bold = ImageTk.PhotoImage((Image.open('./icons/b.png')).resize((31, 31)))
# Obtaining the system-dependent background color value of the button to disable square-shaped 
# highlighting ot the buttons with images when the mouse is hovered over them.
default_button_color = font_picker_opener['bg']

bold_button = Button(toolbar_frame, image=img_bold, command=text_to_bold, borderwidth=0,
                     activebackground=default_button_color, highlightbackground=default_button_color,
                     highlightthickness=0)
bold_button.grid(row=0, column=0, padx=(6, 0))
tooltip_bold = ToolTip(bold_button, msg="Bold")

img_italics = ImageTk.PhotoImage((Image.open('./icons/i.png')).resize((32, 32)))
italics_button = Button(toolbar_frame, image=img_italics, command=text_to_italics, borderwidth=0,
                        activebackground=default_button_color, highlightbackground=default_button_color,
                        highlightthickness=0)
italics_button.grid(row=0, column=1, padx=(0, 3))
tooltip_italics = ToolTip(italics_button, msg='Italics')

# Sizes menu
font_size_options = [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36]
font_size = StringVar(toolbar_frame)
font_size.set(set_font['size'])
font_size_menu = ttk.Combobox(toolbar_frame, font=('Sarai', 16), textvariable=font_size, values=font_size_options, width=4, takefocus=0, state='readonly')
font_size_menu.grid(row=0, column=3, padx=(13, 11))
font_size_menu.bind("<<ComboboxSelected>>", apply_font_size_change)


ttk.Style().configure('TCombobox', relief='groove', selectbackground=default_button_color, selectforeground='',
                      fieldbackground=default_button_color,
                      activebackground=default_button_color,
                      highlightforeground=default_button_color, highlightthickness=0)

img_rgb = ImageTk.PhotoImage(Image.open(('./icons/rgb.png')).resize((33, 33)))
# for toggling on-off state
global is_colored
is_colored = False
apply_palette_button = Button(toolbar_frame, image=img_rgb, command=apply_color, borderwidth=0,
                      activebackground=default_button_color, highlightbackground=default_button_color,
                      highlightthickness=0)
apply_palette_button.grid(row=0, column=5)
tooltip_apply_palette = ToolTip(apply_palette_button, msg='Применить палитру')

img_lang = ImageTk.PhotoImage(Image.open(('./icons/lang.png')).resize((37, 37)))
language_button = Button(toolbar_frame, image=img_lang, command=detect_language, borderwidth=0,
                      activebackground=default_button_color, highlightbackground=default_button_color,
                      highlightthickness=0)
language_button.grid(row=0, column=4, padx=(0, 11))
tooltip_language_button = ToolTip(language_button, msg='Определить язык')


# Menu
top_menu = Menu(root)
root.config(menu=top_menu)

# Menu options
menu_option_file = Menu(top_menu, tearoff=False)

top_menu.add_cascade(label='Файл', menu=menu_option_file)
menu_option_file.add_command(label='Создать')
menu_option_file.add_command(label='Открыть', command=load_file)
menu_option_file.add_command(label='Сохранить как...', command=save_file_as)
menu_option_file.add_command(label='Закрыть', command=close_file)
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


# configuring key shortcut
root.bind('<Control-A>', select_all)

# Status bar
status_bar = Label(root, text='', anchor=E)
status_bar.pack(fill=X, side=BOTTOM, pady=5)

fonts = get_fonts()

font_popup = Popup(title='Выбрать шрифт', items=fonts,
                   item_selected_callback=apply_font_change,
                   item_inserted_callback=on_font_inserted)


def handle_sigint(sig, frame):
    root.quit()
    root.update()
    print('\nBye!')


def check():
    root.after(200, check)


signal.signal(signal.SIGINT, handle_sigint)
check()

root.mainloop()
