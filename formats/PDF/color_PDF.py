from typing import Iterable

import fitz
from colour import Color
from tables import diff_lvl, color_table

# All the available fonts:
supported_fontnames = [str(fontname) for fontname in fitz.Base14_fontdict.values()]
supported_fontnames.extend([fn for fn in ("Arial", "Times", "Times Roman")])  # additional fonts

# from pymupdf-fonts
installed_fonts = [font['name'] for font in fitz.fitz_fontdescriptors.values()]
supported_fontnames.extend([fn for fn in installed_fonts])


# def scale_fontsize(span):
    # compute new fontsize such that text won't exceed the bbox width
    # curr_fsize = span["size"]
    # text_length = the_font.text_length(text, fontsize=curr_fsize)
    # if text_length <= text_span.width:
    #     return curr_fsize
    # new_size = text_span.width / text_length * curr_fsize  # new fontsize
    # return new_size


def color_letter(letter):
    if letter.lower() in diff_lvl:
        return Color(color_table[letter.lower()]).rgb  # convert hex value into rgb tulpe


def get_text_writers(rect, letters: Iterable[str]) -> dict[str, fitz.TextWriter]:
    """Get dict of TextWriters mapped to letters."""
    return {letter: fitz.TextWriter(rect, color=color_letter(letter)) for letter in color_table}


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
        new_font += 'b' if 'Bold' in used_font else 'it' if 'Italic' in used_font else 'o'
        if new_font not in ('figit', 'figo'):
            new_font += 'i' if 'Italic' in used_font else 'o'
    return new_font


def for_letter(page):
    page_data_blocks = page.get_text('rawdict')
    writers = get_text_writers(page.rect, color_table.keys())

    for block in page_data_blocks['blocks']:
        if block['type']:  # 0 for txt
            continue

        for line in block['lines']:
            # add annotation for removing existing letters
            page.add_redact_annot(contract_selection_field(fitz.Rect(line['bbox'])))
            last_point = None

            for span in line['spans']:
                span_font = fitz.Font(determine_font(span['font']))
                span_font_size = span['size'] * 0.8

                for char in span['chars']:
                    writer = writers.get(char['c'].casefold(), writers['def'])
                    append_to = last_point if last_point else char['origin']
                    writer.append(append_to, char['c'], font=span_font, fontsize=span_font_size)
                    last_point = writer.last_point

    page.apply_redactions()
    for writer in writers.values():
        writer.write_text(page)


fname = 'test.pdf'
doc = fitz.open(fname)
fitz.TOOLS.set_small_glyph_heights(True)
list(map(for_letter, doc.pages(-1)))
doc.save('edited-' + doc.name)
