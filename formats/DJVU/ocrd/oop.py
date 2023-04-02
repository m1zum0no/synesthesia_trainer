import copy
from color_table import color_table
from draft import previous_font

# previous_font & fonts must be initialized once for every document
fonts = set(previous_font)


class Glyph:
    '''Graphic representation of a character, measurements depend on slant/weight/etc attributes, 
    instances of which are grouped into "fonts" for better coordinates substitution of the 
    incorrectly recognized by Tesseract OCR engine char positions'''

    def __init__(self, w, h):
        self.w = w
        self.h = h 


class Font:

    def __init__(self, char=None, glyph: Glyph=None):
        self.glyphs = {} if not glyph else {char: glyph}


    def rearrange_font_glyphs(self, word_bbox, font):
        for char_bbox in word_bbox.validated_chars:
            font.glyphs[char_bbox.char] = word_bbox.font.glyphs.pop(char_bbox.char)

        
    def resolve_font_conflict(self, word_bbox,  char, glyph):
        fonts_with_glyph = list(filter(lambda font: glyph in font, fonts)) or [Font(char, glyph)]
        if len(fonts_with_glyph) > 1:
            for font in fonts_with_glyph:
                if all(char_bbox.glyph == font.glyphs.get(char_bbox.char, char_bbox.glyph) for char_bbox in word_bbox.validated_chars):
                    font.glyphs.update((char_bbox.char, char_bbox.glyph) for char_bbox in word_bbox.validated_chars)
                    return font
            new_font = Font(char, glyph)    
            word_bbox.font.rearrange_font_glyphs(word_bbox, new_font)
            return new_font
        return fonts_with_glyph[0]



class WordBbox():
    '''Contains list of all characters composing word unit and own rightmost coordinates as Tesseract 
    returns correct position on a word-level'''

    def fix_char_positions(self):
        for char_bbox in self.incorrectly_positioned_chars.reverse():
            if glyph := self.font.glyphs[char_bbox.char]:
                char_bbox.glyph = glyph
                self.x1 = char_bbox.x0 = self.x1 - glyph.w
                self.y1 = char_bbox.x0 = self.y1 - glyph.h
                self.incorrectly_positioned_chars.pop(char_bbox)
                # space
        return not self.incorrectly_positioned_chars 


    def ensure_font_consistency(self, glyph, w, h, char):
        if glyph.w != w or glyph.h != h:
            self.font = self.font.resolve_font_conflict(self, char, Glyph(w, h))

    def __init__(self, x0, y0, x1, y1):
        self.x1 = x1
        self.y1 = y1
        self.previous_char_bbox = x0
        self.validated_chars = []
        self.incorrectly_positioned_chars = []
        self.font = previous_font


class CharBbox:
    '''Stores bottom left coordinate of own position on the page and reference 
    to character width and height required by djvumake utility in Glyph class'''

    def validate_coords(self, x0, word_bbox: WordBbox):
        return word_bbox.prev_char_bbox < x0

    def set_glyph(self, x1, y1, word_bbox: WordBbox):
        w = x1 - self.x0
        h = y1 - self.y0
        glyph = word_bbox.font.glyphs.setdefault(self.char, Glyph(w, h))
        word_bbox.ensure_font_consistency(glyph, w, h, self.char) 
        return word_bbox.font.glyphs[self.char]

    def __init__(self, x0, y0, x1, y1, char, word_bbox: WordBbox):
        self.char = char
        if self.validate_coords(x0, word_bbox):
            self.x0 = x0
            self.y0 = y0
            self.glyph = self.set_glyph(x1, y1, word_bbox)
            word_bbox.previous_char_bbox = x1
            word_bbox.validated_chars.append(self)
        else:
            self.x0 = None
            self.y0 = None
            self.glyph = None
            word_bbox.incorrectly_positioned_chars.append(self)
