# -*- coding: utf-8 -*-
"""
@author: jcuesta
"""


#### 1. Librería pdfplumber 

import pdfplumber

with pdfplumber.open("C:\\ruta\\archivo.pdf") as pdf:
    first_page = pdf.pages[0]
    print(first_page.extract_text())
   

#### 2. Librería textract

import textract
PDF_read = textract.process("C:\\ruta\\archivo.pdf")

#### 3. Librería tabula

from tabula.io import read_pdf
dfs = read_pdf("C:\\ruta\\archivo.pdf", pages='all')

#### 4. Libreria pdfminer

from pdfminer.high_level import extract_text
text = extract_text("C:\\ruta\\archivo.pdf")


#### 5. Libreria PyPDF2

from PyPDF2 import PdfReader
file = PdfReader("C:\\ruta\\archivo.pdf")
numpages = len(file.pages)
page = file.pages[0]
text = page.extract_text()