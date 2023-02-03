from typing import Iterable
import fitz
from colour import Color
from fitz import TEXT_PRESERVE_LIGATURES, TEXTFLAGS_TEXT
# python3 -m cProfile -stime color_PDF.py  -- timing function
import polyglot   # pip install -U pycld2
from polyglot.detect import Detector
from polyglot.detect.base import *


def bridge_function(color_letter_map, lang):

    # user-defined options
    global color_table, difficulty_lvl, chosen_lang
    color_table = color_letter_map
    chosen_lang = lang

    difficulty_lvl = color_table.keys()
    # user_choice = int of letters for coloring to index letters list

    pdf_filename = 'long.pdf'
    pages_chosen = 10
    driver_code(pdf_filename, pages_chosen)


def init_fonts():
    # store mappings of unsupported fonts onto fallback font with its weight/slant for optimization
    global used_fonts, supported_fontnames
    used_fonts = {}

    # list of all fontnames, supported by the lib
    supported_fontnames = [str(fontname) for fontname in fitz.Base14_fontdict.values()]
    supported_fontnames.extend([fn for fn in ("Arial", "Times", "Times Roman")])

    installed_fonts = [font['name'] for font in fitz.fitz_fontdescriptors.values()]  # from pymupdf-fonts
    supported_fontnames.extend([fn for fn in installed_fonts])


def scale_fontsize(span, new_font):
    prev_fontheight = span['ascender'] - span['descender']
    new_fontheight = new_font.ascender - new_font.descender
    scaling_coeff = prev_fontheight / span['size'] 
    lambda_height = prev_fontheight - new_fontheight
    new_fontsize = span["size"] + lambda_height / scaling_coeff
    return new_fontsize


def color_letter(letter):
    global color_table, difficulty_lvl
    if not isinstance(letter, str):
        return
    if letter.lower() in difficulty_lvl:
        return Color(color_table[letter.lower()]).rgb  # convert hex value to rgb tulpe


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

    text_segment = []
    page_data_blocks = page.get_text('rawdict', flags=TEXTFLAGS_TEXT ^ TEXT_PRESERVE_LIGATURES)

    global color_table
    writers = get_text_writers(page.rect, color_table.keys())
    writers.update({'default': fitz.TextWriter(page.rect, color='#ffffff')})

    if not (page_data_blocks['blocks']):
        return None

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
                    symbol = char['c']

                    # store data from page text segment to test whether the document can be edited reliably
                    text_segment.append(symbol)

                    writer = writers.get(char['c'].casefold(), writers['default'])
                    append_to = last_point if last_point else char['origin']
                    writer.append(append_to, char['c'], font=span_font, fontsize=span_font_size)
                    last_point = writer.last_point

    page.apply_redactions()
    for writer in writers.values():
        writer.write_text(page)

    return ''.join(text_segment)


def has_text(extracted_text, is_editable):
    global chosen_lang
    if extracted_text:
        # print(chosen_lang, Detector(extracted_text).languages[0].name)
        if chosen_lang in [language.name for language in Detector(extracted_text).languages[:3]]:
            is_editable += 1
    return is_editable


def driver_code(pdf_filename, pages_chosen):
    init_fonts()
    pdf = fitz.open(pdf_filename)
    fitz.TOOLS.set_small_glyph_heights(True)

    # leave in memory only the pages that the user have chosen for editing 
    # and discard the rest
    pdf.select([page for page in range(pages_chosen)])

    pdf_volume = pdf.page_count
    is_editable = 0

    for page_num, page in enumerate(pdf):  # .pages
        is_editable = has_text(color_page(page), is_editable)
        if not is_editable and page_num > (pdf_volume / 10 if pdf_volume > 150 else pdf_volume):
            # pdf either doesn't contain the chosen language or is not editable
            # and should be converted to another format
            print('Not editable')
            quit()
    pdf.save('edited-' + pdf.name)
