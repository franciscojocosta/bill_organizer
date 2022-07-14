import PyPDF2
import mysql.connector

def edp():
    pdfFileObj = open("C:\\Users\\franc\\Downloads\\154004959499.pdf", 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    text=''

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

    print (per, " -> ", type(per))


    #Entidade------
    ent_find = 'Data limite de pagamento: '
    ent_find_ix = text.find(ent_find) ## tem 24 caracteres
    ent_find_size = len(ent_find)

    ent_ix = ent_find_ix + ent_find_size
    ent_size = 5
    ent = text[ent_ix : ent_ix + ent_size]
    print (ent, " -> ", type(ent))

    # Referência----------

    ref_ix = ent_ix + ent_size + 2
    ref_size = 11
    ref = text[ref_ix : ref_ix + ref_size].replace(" ","")
    print (ref , " -> ", type(ref))

    # Valor a Pagar

    price_ix = ref_ix + ref_size + 2
    euro_ix = text[price_ix:].find('€')
    price_size = euro_ix - 1
    price = text[price_ix : price_ix + price_size].replace(",",".")
    print (price, " -> ", type(price))

    # Data Limite

    lim_date_ix = price_ix + euro_ix + 2
    lim_date_size = 10
    lim_date = text[lim_date_ix : lim_date_ix + lim_date_size]
    lim_date = lim_date[6:] + "-" + lim_date[3:5] + "-" + lim_date[:2]
    print (lim_date, " -> ", type(lim_date))
    bills = ('EDP','1232432942', float(price), per, int(ent), int(ref), lim_date)
    return bills

def agua():
    pdfFileObj = open("C:\\Users\\franc\\Downloads\\985.AR.DP.141823513.pdf", 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    text=''

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
    price = text[price_ix : price_ix + price_size].replace(",",".")
    print (price)
    # Referência----------

    ref_ix = price_ix + price_size + 1
    ref_size = 11
    ref = text[ref_ix : ref_ix + ref_size].replace(" ","")
    print (ref)

    # Data Limite

    lim_dat_find = 'Data limite pagamento'
    lim_dat_find_ix = text.find(lim_dat_find) ## tem 24 caracteres
    lim_dat_find_size = len(lim_dat_find)

    lim_dat_ix = lim_dat_find_ix + lim_dat_find_size + 1
    lim_dat_size = 11
    lim_date = text[lim_dat_ix : lim_dat_ix + lim_dat_size].replace(" ","-")
    convert ={"jan":"01","feb":"02","mar":"03","abr":"04","mai":"05","jun":"06","jul":"07","ago":"08","set":"09","out":"10","nov":"11","dec":"12"}
    
    for key in convert:
        if key in lim_date:
            val =(convert.get(key))
            break
    
    lim_date = lim_date.replace(key,val)
    lim_date = lim_date[6:] + "-" + lim_date[3:5] + "-" + lim_date[:2]
    print (lim_date)

    bills = ('Agua','1985.AR.DP.141823513', float(price), per, int(ent), int(ref), lim_date)
    return bills
record = edp()


mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="root",
  database="bills"
)

mycursor = mydb.cursor()


val = '122312'
query = "INSERT INTO bills (tipo,id_fatura,price,periodo_fatura,entidade,referencia,data_limite ) VALUES (%s,%s,%s,%s,%s,%s,%s)"
check_fatura_q = """Select COUNT(*) from bills where id_fatura = %s""" %record[1]
mycursor.execute (check_fatura_q)

fatura_entrys = int(mycursor.fetchone()[0])

if fatura_entrys < 1:
    mycursor.execute(query,record)

else:
    print ("Already a bill with this id")

for x in mycursor:
  print(x)
  print ("\n")

mydb.commit()