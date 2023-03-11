# generates file 'color_table.py

import icu
from random import random
from colour import Color


def generate_color_table(lang_charset):
    color_table = {}
    for unicode_char in lang_charset:
        color_table[unicode_char] = Color(hsl=(random() for _ in range(3))).hex
    with open("color_table.py", "w") as output:
        output.write('color_table = ' + str(color_table) + '\n')


def extract_charset(lang_chosen):
    lang_chosen = icu.Locale(lang_chosen)
    lang_unicode_charset = []

    tesseract_code = lang_chosen.getISO3Language()

    try:
        unicodeset = icu.LocaleData(lang_chosen.getName()).getExemplarSet()
    except AttributeError:
        return []

    iter = icu.UnicodeSetIterator(unicodeset)

    for char in iter:
        try:
            lang_unicode_charset.append(char)
        except TypeError:
            pass

    generate_color_table(lang_unicode_charset)


extract_charset('fr')  # locale code
