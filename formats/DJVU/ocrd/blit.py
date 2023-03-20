# if coords for letter are within range of dict letter params, but overlap 
# substitute beginning and ending coords of curr and prev letters 
from color_table import color_table


class Font:
    '''Contains list of all unique instances of the letters within the unicodeset
      of the language for given font'''
    
    pass


class CharDataFont(Font):
    '''Contains list of all unique instances of the letters within the unicodeset,
    their measures, associated color, and font'''

    def __init__(self, char, w, h):
        self._char = char
        self._w = w
        self._h = h
        self._color = color_table.get(self._char.lower(), '#000000')


class Word:
    '''Contains list of all characters composing word'''
    
    def __init__(self, x1, y1, x2, y2):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._prev_x2 = self._x1

    def __determine_font__(self):
        pass    


class Char(Word, CharDataFont):
    '''Stores bottom left coordinate of own position on the page and reference 
    to w/h/color in dict class'''
    
    def __validate_coords__(self, char):
        if Word._prev_x2 < self._x1:
            w = self._x2 - self._x1
            h = self._y2 - self._y1
            # CharDataFont[char] = CharDataFont.get(char, (w, h))
            Word._prev_x2 = self._x1

    def __init__(self, x1, y1, x2, y2, char):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self.__validate_coords__(self, char)
