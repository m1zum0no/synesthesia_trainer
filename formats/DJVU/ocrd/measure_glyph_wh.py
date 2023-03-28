import re
from color_table import color_table
import locale


def color_letters(coords, char):
    global glyphs
    x0, y0, x1, y1 = map(int, coords.split(' '))
    glyph = "'" + char + "': " + ', '.join((str(x1 - x0), str(y1 - y0)))  # w, h
    glyphs.append(glyph)


def parse_letter_positions():
    with open('letters_positions_p67.txt', 'r') as input:
        for line in input.readlines()[2:]:
            global glyphs
            glyphs = [] 
            for char_data in re.finditer(r'char (?P<coords>[0-9 ]+) (?P<char>".")', line):
                color_letters(char_data.group('coords'), char_data.group('char').strip('/"'))
            glyphs_set = sorted(list(set(glyphs)), key=locale.strxfrm)
            for glyph in glyphs_set:
                output.write(glyph + ': ' + str(glyphs.count(glyph)) + '\n')     


locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8') 
with open('glyphs_wh.txt', 'a+') as output:
    parse_letter_positions()

