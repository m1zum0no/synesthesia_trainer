# Generates letters coordinates returned by tesseract and color data in a format recognized by openCV for 
# further visualization
import re
from color_table import color_table


def color_letters(coords, char=''):
    color = color_table.get(char.lower(), '#000000').lstrip('#')   
    color = ' '.join([str(int(color[i:i+2], 16)) for i in (0, 2, 4)])
    output.write(coords + ' ' + color + '\n')


def parse_chars(not_parsed):
    global line
    if next_word := re.search(r'word (?P<coords>[0-9 ]+)', line[not_parsed:]):
        next_word = not_parsed + next_word.span()[0]
    for char_data in re.finditer(r'char (?P<coords>[0-9 ]+) (?P<char>".")', line[not_parsed:next_word]):
        color_letters(char_data.group('coords'), char_data.group('char').strip('/"')) 


def parse_letter_positions():
    with open('letters_positions_p67.txt', 'r') as input:
        global line
        for line in input.readlines()[2:]:
            for word_data in re.finditer(r'word (?P<coords>[0-9 ]+)', line):
                parse_chars(word_data.span()[1])


with open('opencv_formatted_coords.txt', 'a+') as output:
    parse_letter_positions()

