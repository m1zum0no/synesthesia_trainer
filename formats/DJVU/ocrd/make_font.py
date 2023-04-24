#for font in fonts:
#  for char, glyph in font.glyphs.items():
#    print(char, glyph.w, glyph.h)

with open('glyphs.txt', 'r') as input:
    for line in input.readlines():
        data = line.split(' ')
        data[2] = data[2].strip("\n")
        print(f'"{data[0]}": Glyph({data[1]}, {data[2]}), ')