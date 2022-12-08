from tkinter import ttk
from tkinter import *
from popup import Popup
import icu

root = Tk()

# initialize the code - language denomination mapping structure
def map_locale_refs():
    locale_to_lang = {}
    icu_locale_codes = icu.Locale('').getAvailableLocales()
    for locale in icu_locale_codes:
        locale_to_lang[locale] = icu.Locale(locale).getDisplayName()
    return locale_to_lang


def unicode_chars_from_lang(picked_lang):
    update_button_inscription = picked_lang
    button_lang_chooser.config(text=update_button_inscription)
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
            lang_unicode_charset.append(char)  # ord() ?
        except TypeError:
            pass
    print(lang_unicode_charset)


def click_opener():
    lang_choice.deiconify()


locale_mapping = map_locale_refs()

lang_choice = Popup(title='Выбрать язык', items=locale_mapping.values(),
                   item_selected_callback=unicode_chars_from_lang)

button_lang_chooser = Button(root, text='Язык', font='TkDefaultFont', 
                            command=click_opener, relief='sunken')

popup_opened = False  # flag for tracking multiple attempts to open popups
button_lang_chooser.grid(row=0, column=0)

root.mainloop()