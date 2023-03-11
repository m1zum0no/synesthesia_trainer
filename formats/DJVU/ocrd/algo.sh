# djvused myfile.djvu -e 'select 3; size' -- prints size of p3
# DjVu 2479x3508, v24, 300 dpi

# show internal layout data
djvudump les-mots-sartre-texte.djvu 

djvused les-mots-sartre-texte.djvu -e 'select 67; save-page p67.djvu' 
# extract chunks from prev step, incl BG etc
# djvuextract [-page=pagenum] djvufile [chkid=filename]
djvuextract|cjb2 p67.djvu Sjbz=p67.cnk 
# djvuextract p67.djvu Djbz=p67.djbz  

# cd ocrodjvu
python3 ocrodjvu --save-script ../letters_positions_p67.txt -t chars -l=fra ../p67.djvu
python3 ocrodjvu --save-script ../letters_positions_p67.txt -t chars -p=67 -l=fra ../les-mots-sartre-texte.djvu  


# Djbz=p67.djbz
djvumake mod_p67.djvu Sjbz=p67.cnk FGbz=filename|#color:x,y,w,h 
# x,y - координаты верхего левого угла зоны
# djvumake(m) recursively for FGbz chunk
 