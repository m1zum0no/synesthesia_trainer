import fitz

def for_letter(page, text):
    page_data_blocks = page.get_text('rawdict')
    for block in page_data_blocks['blocks']:
        if not block['type']:  # 0 for txt
            for line in block['lines']:
                for span in line["spans"]:
                    #curr_font = span['font']
                    # search the correct fontname  
                    used_font = fitz.Font('Arial')
                    # doc.extractFont(font) for not present 
                    for ch in span['chars']:
                        if ch['c'] == text:
                            letter = ch['c']
                            selection_field = fitz.Rect(ch['bbox']) 
                            #page.add_redact_annot(selection_field)
                            #page.apply_redactions()
                            tw = fitz.TextWriter(page.rect, color=(1, 0, 0))  # color-interpolation-filters="sRGB"
                            tw.append(ch['origin'], letter, font=used_font, fontsize=span["size"])
                            tw.write_text(page)
                        

fname = 'pdf-test.pdf'
text = 'a'
doc = fitz.open(fname)
fitz.TOOLS.set_small_glyph_heights(True)

for page in doc: 
    for_letter(page, text) 

doc.save("marked-" + doc.name)