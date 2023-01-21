import fitz
from colour import Color
from tables import diff_lvl, color_table


# All the available fonts:
supported_fontnames = [str(fontname) for fontname in fitz.Base14_fontdict.values()]
supported_fontnames.extend([fn for fn in ("Arial", "Times", "Times Roman")])  # additional fonts

# from pymupdf-fonts
installed_fonts = [font['name'] for font in fitz.fitz_fontdescriptors.values()]
supported_fontnames.extend([fn for fn in installed_fonts])


def scale_fontsize(span, new_font):
    prev_fontheight = span['ascender'] - span['descender']
    new_fontheight = new_font.ascender - new_font.descender
    scaling_coeff = prev_fontheight / span['size'] 
    lambda_height = prev_fontheight - new_fontheight
    new_fontsize = span["size"] + lambda_height / scaling_coeff
    return new_fontsize


def color_letter(letter):
    if letter.lower() in diff_lvl:
        return Color(color_table[letter.lower()]).rgb  # convert hex value to rgb tulpe


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
    for block in page_data_blocks['blocks']:
        if not block['type']:  # 0 for txt
            for line in block['lines']:
                prev_tw = None
                for span in line['spans']:
                    the_font = fitz.Font(determine_font(span['font']))
                    the_fontsize = scale_fontsize(span, the_font)
                    for ch in span['chars']:
                        # clearing out the spot where letter will be rewritten
                        page.add_redact_annot(contract_selection_field(fitz.Rect(ch['bbox'])))
                        page.apply_redactions()
                        # rewriting the letter in a new color
                        tw = fitz.TextWriter(page.rect, color=color_letter(ch['c']))
                        if prev_tw:
                            # initializing the first element
                            tw.append(prev_tw.last_point, ch['c'], font=the_font, fontsize=the_fontsize)
                        else:
                            tw.append(ch['origin'], ch['c'], font=the_font, fontsize=the_fontsize)
                        tw.write_text(page)
                        prev_tw = tw


fname = 'long.pdf'
doc = fitz.open(fname)
fitz.TOOLS.set_small_glyph_heights(True)
list(map(for_letter, doc.pages(-1)))
doc.save('edited-' + doc.name)
