###########Preparation step:###########
# show internal layout data (chunkIDs)
djvudump file.djvu 

# print size of page N, dpi for INFO
djvused myfile.djvu -e 'select N; size'

# save page as a separate document 
# usable but might replicate references if multiple; to avoid references - 'save-page'
djvused file.djvu -e 'select N; save-page-with pN.djvu'

# extract chunks from single page DJVU, including BG44 for djvumakem
# extensions: Sjbz=.cnk, Djbz=.djbz
# cjb2 can be used instead of djvuextract for Sjbz
djvuextract [-page=pagenum] djvufile [chkid=filename] 


###########Generate .txt file with characters positions:###########
# cd ocrodjvu
python3 ocrodjvu --save-script ../out.txt -t chars -l=fra ../pN.djvu
python3 ocrodjvu --save-script ../out.txt -t chars -p=N -l=fra ../file.djvu

# obtain FGbz 
djvumake edited-pN.djvu Sjbz=pN.cnk FGbz=filename|#color:x,y,w,h 
# x,y - координаты верхего левого угла зоны

# to color recursively:
# djvumakem edited-pN.djvu INFO=,,300 INCL=?.djbz Sjbz=Sjbz.cnk FGbz_old=FGbz.cnk FGbz= BG44=BG44.cnk


###########OpenCV and djvumakem:###########
# generate .djvu from .pdf
pdf2djvu -o file.djvu file.pdf

# convert a page to .tiff for OpenCV 
ddjvu -format=tiff -page=N file.djvu pN.tiff 

#for encoding FGbz_old: FGbz=bzzfile
bzz -e input output 
