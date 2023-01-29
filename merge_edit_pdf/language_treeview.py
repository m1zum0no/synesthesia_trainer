from tkinter import *
from popup import Popup
import icu
# for generate_color_table()
from random import random
from colour import Color
from test_color import *


def generate_color_table(lang_charset):
    global color_table
    for unicode_char in lang_charset:
        color_table[unicode_char] = Color(hsl=(random() for _ in range(3))).hex
    driver_code(color_table)


# initialize the code - language denomination mapping structure
def map_locale_refs():
    locale_to_lang = {}
    icu_locale_codes = icu.Locale('').getAvailableLocales()
    for locale in icu_locale_codes:
        locale_to_lang[locale] = icu.Locale(locale).getDisplayName()
    return locale_to_lang


def unicode_chars_from_lang(picked_lang):
    update_button_inscription = picked_lang
    global button_lang_chooser
    button_lang_chooser.config(text=update_button_inscription)

    global root
    root.destroy()

    global color_table
    color_table = {}
    global locale_mapping
    for locale_code, lang_name in locale_mapping.items():
        if picked_lang == locale_mapping[locale_code]:
            picked_lang = locale_code
    picked_lang = icu.Locale(picked_lang)
    lang_unicode_charset = []
    try:
        unicodeset = icu.LocaleData(picked_lang.getName()).getExemplarSet()
    except AttributeError:
        return []
    iter = icu.UnicodeSetIterator(unicodeset)
    for char in iter:
        try:
            lang_unicode_charset.append(ord(char))
        except TypeError:
            pass
    generate_color_table(lang_unicode_charset)


def click_opener():
    global lang_choice
    lang_choice.deiconify()


def determine_language():
    global root
    root = Tk()

    global locale_mapping
    locale_mapping = map_locale_refs()
    locale_mapping_unique = {code: lang for code, lang in locale_mapping.items() if '_' not in code}

    global lang_choice
    lang_choice = Popup(title='Выбрать язык', items=locale_mapping_unique.values(),
                        item_selected_callback=unicode_chars_from_lang)
  
    global button_lang_chooser
    button_lang_chooser = Button(root, text='Язык', font='TkDefaultFont', 
                                command=click_opener, relief='sunken')

    button_lang_chooser.grid(row=0, column=0)
    root.mainloop()


determine_language()