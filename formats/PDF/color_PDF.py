import fitz
from colour import Color
from prog import diff_lvl, color_table

# All the available fonts:
supported_fontnames = [str(fontname) for fontname in fitz.Base14_fontdict.values()]
for def_fontname in ("Arial", "Times", "Times Roman"):  # additional fonts  
    supported_fontnames.append(def_fontname)

# from pymupdf-fonts
installed_fonts = [font['name'] for font in fitz.fitz_fontdescriptors.values()]
for ext_fontname in installed_fonts:
    supported_fontnames.append(ext_fontname)


# if replace_font, ignore the level parameter and reqrite all letters in a new font 
def for_letter(page, text):
    page_data_blocks = page.get_text('rawdict')
    for block in page_data_blocks['blocks']:
        if not block['type']:  # 0 for txt
            for line in block['lines']:
                for span in line["spans"]:
                    try:  # searching for the canonic fontname 
                        doc_font = next(fontname for fontname in supported_fontnames \
                            if fontname.casefold() in span['font'].casefold())
                    except StopIteration:  # replace text with fallback font if none found
                        #doc_font = 'fallback_font'
                        replace_font = True
                        pass
                        # rewrite all the documnets to match the existing font
                    the_font = fitz.Font(doc_font) 
                    for ch in span['chars']:
                        if ch['c'].lower() in diff_lvl:
                            letter = ch['c']
                            clr = Color(color_table[letter.lower()]).rgb  # convert hex value into rgb tulpe
                            rect = fitz.Rect(ch['bbox'])
                            # scaling down the selection field
                            # to avoid selecting surrounding letters
                            selection_field = +rect 
                            selection_field.y0 += rect.height * 0.4
                            selection_field.y1 = selection_field.y0 + rect.height * 0.2
                            # clearing out selected field 
                            page.add_redact_annot(selection_field)
                            page.apply_redactions()
                            # rewriting the letter in a new color
                            tw = fitz.TextWriter(page.rect, color=clr)
                            tw.append(ch['origin'], letter, font=the_font, fontsize=span["size"])
                            tw.write_text(page)
                        

fname = 'pdf-test.pdf'
text = 'a'
doc = fitz.open(fname)
fitz.TOOLS.set_small_glyph_heights(True)

for page in doc: 
    for_letter(page, text) 

doc.save('edited-' + doc.name)