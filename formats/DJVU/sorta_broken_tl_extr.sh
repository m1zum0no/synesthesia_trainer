# Extract DJVU hidden text layer as PDF
# privided at https://superuser.com/questions/808847/djvu-hidden-text-%E2%86%92-pdf

# Convert the DjVu to PDF with the OCR layer preserved in the PDF. Then run:
gs -q -o - -dFILTERIMAGE -sDEVICE=pdfwrite -f "${input_pdf}" | pdftk - output - uncompress | sed "s/^3 Tr$/0 Tr/g" | pdftk - output "${output_pdf}" compress
# where the user specifies ${input_pdf} and ${output_pdf}. 
# gs removes (-dFILTERIMAGE) all the images, and sed makes it so the PDF renders the hidden OCR text as visible 
# (by changing PDF's 3 Tr or "hidden text render" command to 0 Tr or "default text render"). 
# The last pdftk command isn't strictly necessary, but the first one is, else sed wouldn't be able to change the PDF
# Tr command.