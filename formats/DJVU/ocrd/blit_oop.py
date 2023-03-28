# parse the output of ocrodjvu utility which is based on Tesseract OCR engine 
# Tesseract deternines the bounding boxes 'bbox' of each char it recgnizes 

import re
from color_table import color_table
from oop import CharBbox, WordBbox


def parse_chars(coords, char):
    char = CharBbox(*map(int, coords.split(' ')))


def parse_words():
    with open('letters_positions_p67.txt', 'r') as input:
        global line
        for line in input.readlines()[2:]:
            for word_data in re.finditer(r'word (?P<coords>[0-9 ]+)', line):
                word = WordBbox(*map(int, word_data.group('coords').split(' ')[:-1]))  # excluding '' as last lst arg returned by group 
                curr_word_start = word_data.span()[1]
                # word that's currently being parsed ends where new one starts or is the last
                if next_word := re.search(r'word (?P<coords>[0-9 ]+)', line[curr_word_start:]):
                    next_word = curr_word_start + next_word.span()[0]
                for char_data in re.finditer(r'char (?P<coords>[0-9 ]+) (?P<char>".")', line[curr_word_start:next_word]):
                    parse_chars(char_data.group('coords'), char_data.group('char').strip('/"'))


with open('v5_opencv_input.txt', 'a+') as output:
    parse_words()