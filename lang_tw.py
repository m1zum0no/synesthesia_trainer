from tkinter import *
from popup import Popup
import icu

root = Tk()

# def map_locale_refs():
#     icu_locale_codes = icu.Locale('').getAvailableLocales()
#     locale_to_lang = {code: icu.Locale(code).getDisplayName() for code in icu_locale_codes if '_' not in code}
#     return locale_to_lang


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
locale_mapping_unique = {code: lang for code, lang in locale_mapping.items() if '_' not in code}

lang_choice = Popup(title='Выбрать язык', items=locale_mapping_unique.values(),
                    item_selected_callback=unicode_chars_from_lang)

button_lang_chooser = Button(root, text='Язык', font='TkDefaultFont', 
                            command=click_opener, relief='sunken')

button_lang_chooser.grid(row=0, column=0)


##################################################################################
# from hashlib import sha256
#
# locale_mapping_unique1 = {code: lang for code, lang in locale_mapping.items() if '_' not in code}
#
# locale_mapping_unique2 = {}
# locale_mapping_duplicates = {}
# charset_hashes = set()
#
# for code, lang in locale_mapping.items():
#     charset = icu.LocaleData(code).getExemplarSet()
#     hash = sha256(str(charset).encode('utf8')).hexdigest()
#     if hash not in charset_hashes:
#         locale_mapping_unique2[code] = lang
#         charset_hashes.add(hash)
#
#         locale_mapping_duplicates[hash] = [lang]
#     else:
#         locale_mapping_duplicates[hash].append(lang)
#
# for key in list(locale_mapping_duplicates.keys()):
#     if len(locale_mapping_duplicates[key]) == 1:
#         del locale_mapping_duplicates[key]
##################################################################################

root.mainloop()