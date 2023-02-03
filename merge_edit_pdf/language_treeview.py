from tkinter import *
from popup import *
import icu
# for generate_color_table()
from random import random
from colour import Color
from test_color import *


def generate_color_table(lang_charset):
    global lang_chosen
    for unicode_char in lang_charset:
        color_table[unicode_char] = Color(hsl=(random() for _ in range(3))).hex
    bridge_function(color_table, lang_chosen)
    root.destroy()
    print(lang_chosen)
    print(color_table)


def map_locale_refs():
    locale_to_lang = {}
    icu_locale_codes = icu.Locale('').getAvailableLocales()
    for locale in icu_locale_codes:
        locale_to_lang[locale] = icu.Locale(locale).getDisplayName()
    return locale_to_lang


def extract_charset(selected_item):
    global lang_chosen
    lang_chosen = selected_item

    update_button_inscription = lang_chosen
    button_lang_chooser.config(text=update_button_inscription)

    for locale_code, lang_name in locale_mapping.items():
        if selected_item == locale_mapping[locale_code]:
            selected_item = locale_code

    selected_item = icu.Locale(selected_item)
    lang_unicode_charset = []

    try:
        unicodeset = icu.LocaleData(selected_item.getName()).getExemplarSet()
    except AttributeError:
        return []

    iter = icu.UnicodeSetIterator(unicodeset)

    for char in iter:
        try:
            lang_unicode_charset.append(char)
        except TypeError:
            pass

    generate_color_table(lang_unicode_charset)


def click_opener():
    lang_choice.deiconify()


root = Tk()

color_table = {}

locale_mapping = map_locale_refs()
locale_mapping_unique = {code: lang for code, lang in locale_mapping.items() if '_' not in code}

lang_choice = Popup(title='Выбрать язык', items=locale_mapping_unique.values(),
                    item_selected_callback=extract_charset)

button_lang_chooser = Button(root, text='Язык', font='TkDefaultFont',
                            command=click_opener, relief='sunken')

button_lang_chooser.grid(row=0, column=0)

root.mainloop()
