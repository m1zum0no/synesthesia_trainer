import re
from color_table import color_table
from oop import *


awaits_glyphs = []


with open('p67.fgbz', 'a+') as output:
    with open('letters_positions_p67.txt', 'r') as input:
        for line in input.readlines()[2:]:
            previous_font = Font()
            for word_data in re.finditer(r'word (?P<coords>[0-9 ]+)', line):
                word_bbox = WordBbox(*map(int, word_data.group('coords').split(' ')[:-1]))
                word_start = word_data.span()[1]
                if next_word := re.search(r'word (?P<coords>[0-9 ]+)', line[word_start:]):
                    next_word = word_start + next_word.span()[0]
                for char_data in re.finditer(r'char (?P<coords>[0-9 ]+) (?P<char>".")', line[word_start:next_word]):
                    char_bbox = CharBbox(*map(int, char_data.group('coords').split(' ')), char_data.group('char').strip('/"'), word_bbox)
                    if not word_bbox.incorrectly_positioned_chars():
                        output.write(color_table[char_bbox.char], ':', ','.join(map(str, (char_bbox.x0, char_bbox.y0, char_bbox.glyph.w, char_bbox.glyph.h))))
                if word_bbox.incorrectly_positioned_chars():
                    if not word_bbox.fix_char_positions():
                        awaits_glyphs.append(word_bbox)
                previous_font = word_bbox.font()  
