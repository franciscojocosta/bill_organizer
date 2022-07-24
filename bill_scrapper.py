
import PyPDF2
import mysql.connector
import os
import sys
from pickle import TRUE
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
 
logging.basicConfig(filename='log.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

record = (0,0) ## Variable to store bill data
src_path = 'C:\\Users\\franc\\Downloads'  #### Path to check for bills

class MonitorFolder(FileSystemEventHandler):
    ## When downloading bills, observer gets multiple entrys of filename, filename_aux variable validates if filename already processed.
    filename_aux = ""

    def edpmatch(self,filename):
        ### EDP bill names has 12 integers at the begging
        if len(filename) < 12:  
            return False

        for i in range(12):
            if filename[i].isnumeric() == False: 
                break
            
            if i == 11 and self.filename_aux != filename:  
                
                if len(filename) < 22 and ".pdf" in filename: 
                    self.filename_aux = filename
                    return True
               
    def aguamatch(self,filename):
        
        if "985.AR.DP." in filename and filename != self.filename_aux:
            self.filename_aux = filename
            return TRUE

    def get_agua(self, filename,filepath): 
        logging.info('Bill: %s is being processed', filename)
        bill_handler('agua',filepath)

    def get_edp(self, filename,filepath): 
        logging.info('Bill: %s is being processed', filename)
        bill_handler('EDP',filepath)

    def on_modified(self, event):

        filepath = event.src_path
        filename = os.path.basename(filepath)

        if self.aguamatch(filename): self.get_agua(filename, filepath)

        elif self.edpmatch(filename): self.get_edp(filename, filepath)

        else: pass

class bill_handler():

    def edp(self,filepath):

        filename = os.path.basename(filepath) # Get filename from filepath

        try:
            pdfFileObj = open(filepath, 'rb')
        except OSError:
            logging.error('Cannot open bill file')
            sys.exit()

        with pdfFileObj:
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            text=''
            pageObj = pdfReader.getPage(pdfReader.numPages - 1) ## Get only last Page. Where Bills info is at.
            text=text+pageObj.extractText()

        #Periodo de facturação

        per_find ='Período de faturação: '
        per_find_ix = text.find(per_find)
        per_find_size = len(per_find)
        per_ix = per_find_ix + per_find_size
        per_y1_ix = text[per_ix:].find('202')
        per_y2_ix = text[per_ix + per_y1_ix +1 :].find('202')
        per_size = per_y1_ix + per_y2_ix + 5
        per = text[per_ix : per_ix + per_size]

        #Entidade

        ent_find = 'Data limite de pagamento: '
        ent_find_ix = text.find(ent_find) ## tem 24 caracteres
        ent_find_size = len(ent_find)
        ent_ix = ent_find_ix + ent_find_size
        ent_size = 5
        ent = text[ent_ix : ent_ix + ent_size]

        # Referência

        ref_ix = ent_ix + ent_size + 2
        ref_size = 11
        ref = text[ref_ix : ref_ix + ref_size].replace(" ","")

        # Valor a Pagar

        price_ix = ref_ix + ref_size + 2
        euro_ix = text[price_ix:].find('€')
        price_size = euro_ix - 1
        price = text[price_ix : price_ix + price_size].replace(",",".")

        # Data Limite

        lim_date_ix = price_ix + euro_ix + 2
        lim_date_size = 10
        lim_date = text[lim_date_ix : lim_date_ix + lim_date_size]
        lim_date = lim_date[6:] + "-" + lim_date[3:5] + "-" + lim_date[:2]

        ### Gather all information

        bills = ('EDP',filename[0:12], float(price), per, int(ent), int(ref), lim_date)

        return bills

    def agua(self,filepath): 
        
        filename = os.path.basename(filepath)

        try:
            pdfFileObj = open(filepath, 'rb')
        except OSError:
            logging.error('Cannot open bill file')
            sys.exit()
        with pdfFileObj:
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            text=''
            pageObj = pdfReader.getPage(0) ## Get only first Page. Where Bills info is at.
            text=text+pageObj.extractText()
        
        #Periodo de facturação

        per_find ='Resumo de faturação Período Faturação: '
        per_find_ix = text.find(per_find)
        per_find_size = len(per_find)
        per_ix = per_find_ix + per_find_size
        per_size = 23
        per = text[per_ix : per_ix + per_size]

        #Entidade

        ent_find = 'do Credor (IDC) PT20110442.'
        ent_find_ix = text.find(ent_find) ## tem 24 caracteres
        ent_find_size = len(ent_find)
        ent_ix = ent_find_ix + ent_find_size + 1
        ent_size = 5
        ent = text[ent_ix : ent_ix + ent_size]

        # Valor a Pagar

        price_ix = ent_ix + ent_size + 1
        euro_ix = text[price_ix:].find('€')
        price_size = euro_ix
        price = text[price_ix : price_ix + price_size].replace(",",".")

        # Referência

        ref_ix = price_ix + price_size + 1
        ref_size = 11
        ref = text[ref_ix : ref_ix + ref_size].replace(" ","")

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
            else:
                val = "00"

        lim_date = lim_date.replace(key,val)
        lim_date = lim_date[6:] + "-" + lim_date[3:5] + "-" + lim_date[:2]
        
        ### Gather all information

        bills = ('Agua',filename[0:19], float(price), per, int(ent), int(ref), lim_date)

        return bills

    def store_bill(self,tipo,filepath):
        ### DB connection
        try:
            mydb = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="root",
                database="bills"
                )

        except mysql.connector.Error as err:
            logging.error('Cant connect to DB : %s', err)
        ###

        if tipo == 'EDP':
            record = self.edp(filepath)
        elif tipo == 'agua':
            record = self.agua(filepath)
        else: record = 0

        #### Create query to insert bill into DB
        mycursor = mydb.cursor()
        query = "INSERT INTO bills (tipo,id_fatura,price,periodo_fatura,entidade,referencia,data_limite ) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        
        #### Create query to check for duplicates in DB
        check_fatura_q = """Select COUNT(*) from bills where id_fatura = '%s'""" %(record[1])
        try:
            mycursor.execute(check_fatura_q)
            fatura_entrys = int(mycursor.fetchone()[0])
        except:
            logging.error('Error on check fatura query')
            pass
        
        if fatura_entrys < 1: ## 
            try:
                mycursor.execute(query,record)
            except:
                logging.error('Error on fatura query')
                pass
            logging.info('Bill stored %s', record)

        else:
            logging.warning('Already a bill with this id.')

        mydb.commit()
        mycursor.close()

    def __init__(self, tipo, filepath):
        
        self.store_bill(tipo,filepath)

if __name__ == "__main__":
    
    event_handler=MonitorFolder()
    observer = Observer()
    observer.schedule(event_handler, path=src_path, recursive=True)
    observer.start()
    
    logging.info('Monitoring Started')
    
    try:
        while(True):
           time.sleep(1)
           
    except KeyboardInterrupt:
            observer.stop()
            observer.join()


