import re
from color_table import color_table
from fgbz_classes import WordBbox, Font, CharBbox
#from previous_font import previous_font


fonts = set()
# previous_font & fonts must be initialized once for every document
previous_font = Font()
fonts.add(previous_font)


with open('glyphs.txt', 'a+') as output:
  with open('debug_positions.txt', 'r') as input:
    for line in input.readlines()[2:]:
      distance_between_char_bboxes = 3
      for word_data in re.finditer(r'word (?P<coords>[0-9 ]+)', line):
        word_coords = list(map(int, word_data.group('coords').split(' ')[:-1]))
        x0 = word_coords[0] = word_coords[0] + distance_between_char_bboxes  
        x1 = word_coords[2] = word_coords[2] + distance_between_char_bboxes   
        word_bbox = WordBbox(*word_coords, previous_font)
        word_start = word_data.span()[1]
        if next_word := re.search(r'word (?P<coords>[0-9 ]+)', line[word_start:]):
          next_word = word_start + next_word.span()[0]
          for char_data in re.finditer(r'char (?P<coords>[0-9 ]+) (?P<char>".")', line[word_start:next_word]):
            char_coords = list(map(int, char_data.group('coords').split(' ')))
            x0 = char_coords[0] = char_coords[0] + distance_between_char_bboxes
            x1 = char_coords[2] = char_coords[2] - distance_between_char_bboxes  
            y0, y1 = char_coords[1], char_coords[3]

            if word_bbox.chars:
              prev_char = word_bbox.chars[-1]

              if prev_char.left_coords_from_next_char or hasattr(prev_char, 'maybe_left_coords_from_next_char'):
                if not prev_char.left_coords_from_next_char:
                  prev_char.left_coords_from_next_char = True
                word_bbox.previous_char_bbox = x1
                prev_char.x0 = x0
                prev_char.y0 = y0
                prev_char.h = y1 - prev_char.y0
                char_bbox = CharBbox(char_data.group('char').strip('/"'), word_bbox, fonts)
                char_bbox.corrected_coords = True
                if prev_char.w and ((prev_char.w == (x1 - x0)) and ((y1 - y0 - word_bbox.font.glyphs.get(prev_char.char, prev_char).h) in range(-2, 2))):  
                  # curr char bbox is for previous char
                  char_bbox.left_coords_from_next_char = True
                  char_bbox.overlap_preceeds = False
                elif prev_char.w:  
                  char_bbox.y0 = y0
                  char_bbox.x1 = x1
                  char_bbox.y1 = y1
                  char_bbox.h = char_bbox.y1 - char_bbox.y0
                  if not char_bbox.w:
                    char_bbox.w = char_bbox.x1 - (prev_char.x0 + prev_char.w + distance_between_char_bboxes * 2)
                  char_bbox.x0 = char_bbox.x1 - char_bbox.w
                  char_bbox.overlap_preceeds = False
                continue
            char_bbox = CharBbox(char_data.group('char').strip('/"'), word_bbox, fonts, *char_coords) 
          word_bbox.expand_font()
          for char_bbox in word_bbox.chars:
            w, h = (char_bbox.glyph.w, char_bbox.glyph.h) if hasattr(char_bbox, 'glyph') else (char_bbox.w, char_bbox.h)
            char_position_and_color = color_table.get(char_bbox.char.lower(), '#000000') + ':' + ','.join(map(str, (char_bbox.x0, char_bbox.y0, w, h)))
            #output.write
            print(char_position_and_color, end='')
          word_bbox.chars.clear()
          previous_font = word_bbox.font