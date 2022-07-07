import PyPDF2

pdfFileObj = open("C:\\Users\\franc\\Downloads\\Detalhe_517097797_2022_02.pdf", 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
text=''

for i in range(0,pdfReader.numPages):
 #    creating a page object
    pageObj = pdfReader.getPage(i)
   #  extracting text from page
    text=text+pageObj.extractText()
print(text)