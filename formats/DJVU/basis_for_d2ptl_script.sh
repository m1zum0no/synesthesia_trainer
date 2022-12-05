#!/bin/bash

djvu2hocr -p 10 sample.djvu | sed 's/ocrx/ocr/g' > pg10.html

ddjvu -format=tiff -page=10 sample.djvu pg10.tif

pdfbeads -o pg10.pdf