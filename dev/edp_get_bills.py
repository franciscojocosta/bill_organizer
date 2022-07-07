import PyPDF2

pdfFileObj = open("C:\\Users\\franc\\Downloads\\154004959499.pdf", 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
text=''
'''
Função para extrair dados da EDP
Output: 
  - Preço a pagar            - Check
  - Periódo de facturação    - Check
  - Entidade                 - Check
  - Referência               - Check
  - Data limite              - Check

  138005005482.pdf
  174004775843.pdf
  218002263708.pdf
  184003884546.pdf
  198003152531.pdf
  196003675869.pdf
  154004959499.pdf

'''
pageObj = pdfReader.getPage(pdfReader.numPages - 1) ## Get only last Page. Where Bills info is at.
    
text=text+pageObj.extractText()

#Periodo de facturação------
per_find ='Período de faturação: '
per_find_ix = text.find(per_find)
per_find_size = len(per_find)
per_ix = per_find_ix + per_find_size
per_y1_ix = text[per_ix:].find('202')

per_y2_ix = text[per_ix + per_y1_ix +1 :].find('202')
per_size = per_y1_ix + per_y2_ix + 5
per = text[per_ix : per_ix + per_size]

print (per)


#Entidade------
ent_find = 'Data limite de pagamento: '
ent_find_ix = text.find(ent_find) ## tem 24 caracteres
ent_find_size = len(ent_find)

ent_ix = ent_find_ix + ent_find_size
ent_size = 5
ent = text[ent_ix : ent_ix + ent_size]
print (ent)

# Referência----------

ref_ix = ent_ix + ent_size + 2
ref_size = 11
ref = text[ref_ix : ref_ix + ref_size]
print (ref)

# Valor a Pagar

price_ix = ref_ix + ref_size + 2
euro_ix = text[price_ix:].find('€')
price_size = euro_ix - 1
price = text[price_ix : price_ix + price_size]
print (price)

# Data Limite

lim_date_ix = price_ix + euro_ix + 2
lim_date_size = 10
lim_date = text[lim_date_ix : lim_date_ix + lim_date_size]
print (lim_date)