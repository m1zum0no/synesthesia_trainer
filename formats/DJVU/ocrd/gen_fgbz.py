import re
from color_table import color_table


def color_letters(letters_in_list):
    with open('p67.fgbz', 'a+') as output:
        for letter in letters_in_list:
            coords = [int(coord) for coord in letter[:4]]
            coords = [coords[0], coords[1], coords[2] - coords[0], coords[3] - coords[1]]
            output.write(color_table.get(letter[4].lower(), '#000000') + ':' + ','.join(str(coord) for coord in coords))


def parse_letter_positions():
    with open('letters_positions_p67.txt', 'r') as input:
        for line in input.readlines()[2:]:
            color_letters([[y.strip('\"')
                            for y in x.group()[5:-1].split(' ')]
                          for x in re.finditer(r'char (.*?)\)', line)])


parse_letter_positions()