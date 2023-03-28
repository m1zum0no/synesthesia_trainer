from color_table import color_table

class Glyph:
    def __init__(self, w, h, char):
        self.w = w
        self.h = h 
        self.color = color_table[char]


class Font:
    #self.glyphs 
    pass


class CharBbox:
    def validate_coords(self, word: WordBbox, font: Font, char):
        if word.prev_char_bbox < self.x0:
            w = self.x1 - self.x0
            h = self.y1 - self.y0
            self.glyph = font.glyphs[char] = font.glyphs.get(char, (w, h))  # d.setdefault
            word.prev_char_bbox = self.x1

    def __init__(self, x0, y0, x1, y1, char):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.validate_coords(self, word, font, char)
    


class WordBbox():
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0  # ?
        self.x1 = x1
        self.y1 = y1
        # initialize the x1 coordinate of the previous char with the value of 
        # left corner of first char in the word 
        self.prev_char_bbox = self.x0

    def determine_font(self):
        pass

