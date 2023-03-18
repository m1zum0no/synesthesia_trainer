# Generates letters coordinates returned by tesseract and color data in a format recognized by openCV for 
# further visualization
import re
from color_table import color_table


def color_letters(coords, char):
    global word
    bgr_color = color_table.get(char.lower(), '#000000').lstrip('#')
    bgr_color = [str(int(bgr_color[i:i+2], 16)) for i in (0, 2, 4)][::-1]  # BGR format
    bgr_color = ' '.join(bgr_color)
    output.write(coords + ' ' + bgr_color + ' ' + char + '\n')
    word += char


def parse_chars(word_data):
    global word
    word = ''
    for char_data in re.finditer(r'char (?P<coords>[0-9 ]+) (?P<char>".")', word_data):
        color_letters(char_data.group('coords'), char_data.group('char').strip('/"')) 
    output.write(word + 2*'\n')


def parse_letter_positions():
    with open('letters_positions_p67.txt', 'r') as input:
        for line in input.readlines()[2:]:
            last_word_idx = None
            for word_data in re.finditer(r'word (?P<coords>[0-9 ]+) (?P<char_data>.*?)word', line):
                word_coords = word_data.group('coords')
                output.write(word_coords + '\n')
                parse_chars(word_data.group('char_data'))
                last_word_idx = word_data.span()[1] - 4
            if last_word_idx:
                line = line[last_word_idx:]
                last_word = re.search(r'word (?P<coords>[0-9 ]+)', line)
                last_word_coords = last_word.group('coords')
                output.write(last_word_coords + '\n')
                parse_chars(line[last_word.span()[1]:])
                last_word_idx = None


with open('v5_opencv_input.txt', 'a+') as output:
    parse_letter_positions()

