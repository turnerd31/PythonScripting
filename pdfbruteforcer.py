#a brute force PDF encryption breaker. requires PyPDF2 library. pip install PyPDF2
#requires a word list file
#Created by Drew Turner 4/2019

import PyPDF2

pdf = "C:LOCATION OF ENCRYPTED PDF.pdf"
wordlist = "C:LOCAITON OF WORLDLIST"

pdfReader = PyPDF2.PdfFileReader(open('pdf', 'rb'))

for word in wordlist:
  pdfReader.decrypt('word')
  if (pdfReader.isEncrypted == True):
    print('not the correct password, trying again')
  else : print('correct password found. pdf is decrypted') break
