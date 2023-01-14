import fitz

# figo - FiraGO Regular
# figbo - FiraGO Bold
# figit - FiraGO Italic
# figbi - FiraGO Bold Italic


def fonts_used_within(page):
    global fonts_within_doc 
    for page in doc:
        dict = page.get_text("dict")
        blocks = dict["blocks"]
        for block in blocks:
            if "lines" in block.keys():
                spans = block['lines']
                for span in spans:
                    data = span['spans']
                    for lines in data:
                        fonts_within_doc.append((lines['font']))


def associate_fonts(orig_font):
    f = 'fig'
    f += 'b' if 'Bold' in orig_font else 'it' if 'Italic' in orig_font else 'o'
    if f not in ('figit', 'figo'):
        f += 'i' if 'Italic' in orig_font else 'o'
    if f == 'figo':
        return (f'{f}: figo - FiraGO Regular')
    elif f == 'figbo':
        return f'{f}: figbo - FiraGO Bold'
    elif f == 'figit':
        return f'{f}: figit - FiraGO Italic'
    elif f == 'figbi':
        return f'{f}: figbi - FiraGO Bold Italic'
    else:
        return f


fname = 'long.pdf'
doc = fitz.open(fname)
global fonts_within_doc
fonts_within_doc = []

list(map(fonts_used_within, doc.pages(-10)))

fonts_within_doc = list(dict.fromkeys(fonts_within_doc))

print(*[f'{f}:: {associate_fonts(f)}' for f in fonts_within_doc], sep='\n')
