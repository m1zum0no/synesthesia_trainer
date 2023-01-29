from typing import Iterable
import fitz
from colour import Color
from fitz import TEXT_PRESERVE_LIGATURES, TEXTFLAGS_TEXT
from tables import difficulty_lvl
# python3 -m cProfile -stime color_PDF.py  -- timing function


def scale_fontsize(span, new_font):
    prev_fontheight = span['ascender'] - span['descender']
    new_fontheight = new_font.ascender - new_font.descender
    scaling_coeff = prev_fontheight / span['size'] 
    lambda_height = prev_fontheight - new_fontheight
    new_fontsize = span["size"] + lambda_height / scaling_coeff
    return new_fontsize


def color_letter(letter):
    global color_table
    if letter.lower() in difficulty_lvl:
        return Color(color_table[ord(letter.lower())]).rgb  # convert hex value to rgb tulpe


def get_text_writers(rect, letters: Iterable[str]) -> dict[str, fitz.TextWriter]:
    """Get dict of TextWriters mapped to letters."""
    return {letter: fitz.TextWriter(rect, color=color_letter(letter)) for letter in letters}


def contract_selection_field(letter_span):
    # scaling down the letter selection field
    # to avoid overlap between neighbouring letters
    selection_field = +letter_span
    selection_field.y0 += letter_span.height * 0.4
    selection_field.y1 = selection_field.y0 + letter_span.height * 0.6
    return selection_field


def determine_font(used_font):
    try:
        # check if font used is supported
        new_font = next(fontname for fontname in supported_fontnames
                        if fontname.casefold() in used_font.casefold())
    except StopIteration:
        # else rewrite everything in a fallback font
        new_font = 'fig'

        # figbi figbo figit figo
        new_font += 'bi' if ('Bold' in used_font and 'Italic' in used_font) else \
                    'bo' if ('Bold' in used_font) else \
                    'it' if ('Italic' in used_font) else \
                    'o'
    return new_font


def color_page(page):
    global color_table
    page_data_blocks = page.get_text('rawdict', flags=TEXTFLAGS_TEXT ^ TEXT_PRESERVE_LIGATURES)
    writers = get_text_writers(page.rect, [chr(char_code) for char_code in color_table.keys()])

    for block in page_data_blocks['blocks']:
        if block['type']:  # 0 for txt
            continue

        for line in block['lines']:
            # clear up space for letters to be rewritten
            page.add_redact_annot(contract_selection_field(fitz.Rect(line['bbox'])))
            last_point = None

            for span in line['spans']:
                original_font = span['font']

                if original_font not in used_fonts:
                    used_fonts[original_font] = span_font = fitz.Font(determine_font(original_font))
                else:
                    span_font = used_fonts[original_font]

                span_font_size = span['size'] if span_font == original_font else scale_fontsize(span, span_font)

                for char in span['chars']:
                    writer = writers.get(char['c'].casefold(), fitz.TextWriter(page.rect, color='#000000'))
                    append_to = last_point if last_point else char['origin']
                    writer.append(append_to, char['c'], font=span_font, fontsize=span_font_size)
                    last_point = writer.last_point

    page.apply_redactions()
    for writer in writers.values():
        writer.write_text(page)


def driver_code(table):
    global color_table
    color_table = table


    # user-defined options
    fname = 'long.pdf'
    pages_chosen = 100

    global used_fonts
    used_fonts = {}
    
    # All the available fonts:
    global supported_fontnames
    supported_fontnames = [str(fontname) for fontname in fitz.Base14_fontdict.values()]
    supported_fontnames.extend([fn for fn in ("Arial", "Times", "Times Roman")])  # additional fonts

    # from pymupdf-fonts
    installed_fonts = [font['name'] for font in fitz.fitz_fontdescriptors.values()]
    supported_fontnames.extend([fn for fn in installed_fonts])
    
    global doc
    doc = fitz.open(fname)
    fitz.TOOLS.set_small_glyph_heights(True)
    doc.select([i for i in range(pages_chosen)])
    list(map(color_page, doc.pages()))
    doc.save('edited-' + doc.name)
