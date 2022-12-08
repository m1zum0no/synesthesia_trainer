import icu

# from https://programtalk.com/python-examples/icu.LocaleData.getExemplarSet/
def to_charset(locale):
    glyphs = []
    try:
        unicodeset = icu.LocaleData(locale.getName()).getExemplarSet()
    except AttributeError:
        return []
    iter = icu.UnicodeSetIterator(unicodeset)
    for char in iter:
        try:
            glyphs.append(char)  # ord(
        except TypeError:  # , ex:
            # print char, '=', char[0], char[1], ex
            pass
    return glyphs

locale = icu.Locale("zh_Hans_CN")
#print(locale.getDisplayName())
#print(to_charset(locale))

locales = icu.Locale('').getAvailableLocales()
for key in locales.keys():
    l = icu.Locale(key)
print(l.getDisplayName(l))
print(l.getLocale("Arabic"))


# testing char validity
# import unicodedata
# if unicodedata.category(u"\ua62b") != 'Cn':


# print(locale.getDisplayName(locale)) -- locale name in native language