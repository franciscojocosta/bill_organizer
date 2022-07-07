import PyPDF2

pdfFileObj = open("C:\\Users\\franc\\Downloads\\985.AR.DP.141823513.pdf", 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
text=''
'''
Função para extrair dados da EDP
Output: 
  - Preço a pagar            - 
  - Periódo de facturação    - 
  - Entidade                 - 
  - Referência               - 
  - Data limite              - 

  985.AR.DP.142151485.pdf
  985.AR.DP.141823513.pdf

'''
pageObj = pdfReader.getPage(0) ## Get only first Page. Where Bills info is at.
    
text=text+pageObj.extractText()

#Periodo de facturação------
per_find ='Resumo de faturação Período Faturação: '
per_find_ix = text.find(per_find)
per_find_size = len(per_find)
per_ix = per_find_ix + per_find_size
per_size = 23
per = text[per_ix : per_ix + per_size]

print (per)


#Entidade------
ent_find = 'do Credor (IDC) PT20110442.'
ent_find_ix = text.find(ent_find) ## tem 24 caracteres
ent_find_size = len(ent_find)

ent_ix = ent_find_ix + ent_find_size + 1
ent_size = 5
ent = text[ent_ix : ent_ix + ent_size]
print (ent)

# Valor a Pagar

price_ix = ent_ix + ent_size + 1
euro_ix = text[price_ix:].find('€')
price_size = euro_ix
price = text[price_ix : price_ix + price_size]
print (price)
# Referência----------

ref_ix = price_ix + price_size + 1
ref_size = 11
ref = text[ref_ix : ref_ix + ref_size]
print (ref)

# Data Limite

lim_dat_find = 'Data limite pagamento'
lim_dat_find_ix = text.find(lim_dat_find) ## tem 24 caracteres
lim_dat_find_size = len(lim_dat_find)

lim_dat_ix = lim_dat_find_ix + lim_dat_find_size + 1
lim_dat_size = 11
lim_dat = text[lim_dat_ix : lim_dat_ix + lim_dat_size]
print (lim_dat)
