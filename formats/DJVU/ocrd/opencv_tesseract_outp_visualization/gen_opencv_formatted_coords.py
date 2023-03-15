# Generates letters coordinates returned by tesseract and color data in a format recognized by openCV for 
# further visualization
import re
from color_table import color_table


def color_letters(letters_in_list):
    with open('opencv_input.txt', 'a+') as output:
        for letter in letters_in_list:
            args = [int(coord) for coord in letter[:4]]
            color = color_table.get(letter[4].lower(), '#000000').lstrip('#')
            color = [int(color[i:i+2], 16) for i in (0, 2, 4)][::-1]  # BGR format
            for c in color:
                args.append(c)
            args = [str(a) for a in args]
            args = ' '.join(args)
            output.write(args + '\n')


def parse_letter_positions():
    with open('letters_positions_p67.txt', 'r') as input:
        for line in input.readlines()[2:]:
            color_letters([[y.strip('\"')
                            for y in x.group()[5:-1].split(' ')]
                          for x in re.finditer(r'char (.*?)\)', line)])


parse_letter_positions()
