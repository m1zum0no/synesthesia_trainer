# Generates letters coordinates returned by tesseract and color data in a format recognized by openCV for 
# further visualization
import re
from color_table import color_table
from blit import *


def validate_coords(char, x1, y1, x2, y2):
    pass


def color_letters(coords, char, word_str):
    word_str += char
    validate_coords(char, *coords.split(' '))
    output.write(coords + ' ' + char + '\n')
    return word_str


def parse_chars(not_parsed):
    global line
    word_str = ''
    if next_word := re.search(r'word (?P<coords>[0-9 ]+)', line[not_parsed:]):
        next_word = not_parsed + next_word.span()[0]
    for char_data in re.finditer(r'char (?P<coords>[0-9 ]+) (?P<char>".")', line[not_parsed:next_word]):
        word_str = color_letters(char_data.group('coords'), char_data.group('char').strip('/"'), word_str) 
    output.write(word_str + 2*'\n')


def parse_letter_positions():
    with open('letters_positions_p67.txt', 'r') as input:
        global line
        for line in input.readlines()[2:]:
            for word_data in re.finditer(r'word (?P<coords>[0-9 ]+)', line):
                output.write(word_data.group('coords') + '\n')
                parse_chars(word_data.span()[1])


with open('v5_opencv_input.txt', 'a+') as output:
    parse_letter_positions()
