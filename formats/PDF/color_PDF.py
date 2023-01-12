import fitz
from colour import Color
from tables import diff_lvl, color_table

# All the available fonts:
supported_fontnames = [str(fontname) for fontname in fitz.Base14_fontdict.values()]
supported_fontnames.extend([fn for fn in ("Arial", "Times", "Times Roman")])  # additional fonts

# from pymupdf-fonts
installed_fonts = [font['name'] for font in fitz.fitz_fontdescriptors.values()]
supported_fontnames.extend([fn for fn in installed_fonts])


def for_letter(page):
    page_data_blocks = page.get_text('rawdict')
    for block in page_data_blocks['blocks']:
        if not block['type']:  # 0 for txt
            for line in block['lines']:
                for span in line["spans"]:
                    try:  # searching for the canonic fontname 
                        doc_font = next(fontname for fontname in supported_fontnames \
                                        if fontname.casefold() in span['font'].casefold())
                        doc_font = "notos" 
                    except StopIteration:  # replace font used in the document with a fallback font 
                        # if it's not within the list of supported
                        # doc_font = 'Noto Sans '  # doesn't work cause of stupid codenames
                        # font_weight = [weight for weight in ('Bold', 'Italic') if weight in span['font']]
                        # doc_font += ' '.join(font_weight) if font_weight else 'Regular'
                        # 'Noto Sans Bold', 'Noto Sans Bold Italic', 'Noto Sans Italic', 'Noto Sans Regular'
                        doc_font = "notos"
                    # rewriting all the letters in a new font
                    the_font = fitz.Font(doc_font)
                    for ch in span['chars']:
                        if ch['c'].lower() in diff_lvl:
                            letter = ch['c']
                            if ch['c'] == 'o' or ch['c'] == 'a':
                                print(color_table[ch['c']])
                            clr = Color(color_table[letter.lower()]).rgb  # convert hex value into rgb tulpe
                            rect = fitz.Rect(ch['bbox'])
                            # scaling down the letter selection field
                            # to avoid overlap between neighbouring letters
                            selection_field = +rect 
                            selection_field.y0 += rect.height * 0.4
                            selection_field.y1 = selection_field.y0 + rect.height * 0.2
                            # clearing out selected field 
                            page.add_redact_annot(selection_field)
                            page.apply_redactions()
                            # rewriting the letter in a new color
                            tw = fitz.TextWriter(page.rect, color=clr)
                            tw.append(ch['origin'], letter, font=the_font, fontsize=span["size"]*0.85)
                            tw.write_text(page)


'''
def fonts_used_within(page):
    # check all the fonts instances used within document
    results = []  # list of tuples that store the information as (text, font size, font name) 
    for page in doc:
        dict = page.get_text("dict")
        blocks = dict["blocks"]
        for block in blocks:
            if "lines" in block.keys():
                spans = block['lines']
                for span in spans:
                    data = span['spans']
                    for lines in data:
                        results.append((lines['font']))  # lines['size']
    print(*list(dict.fromkeys(results)), '\n')
'''

fname = 'test.pdf'
doc = fitz.open(fname)
fitz.TOOLS.set_small_glyph_heights(True)
list(map(for_letter, doc))
doc.save('edited-' + doc.name)
