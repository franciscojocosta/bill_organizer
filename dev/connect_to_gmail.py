import imaplib
from typing_extensions import Self
ORG_EMAIL   = "@gmail.com"
FROM_EMAIL  = "franciscojocosta" + ORG_EMAIL
FROM_PWD    = "K5i2EUH2"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993

class Save_Inv:
    
    def __init__(self) -> None:
        print ("Init")
        self.mail = self.connect()
        self.get_data()
    
    def connect(self):
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        print("Connected")
        """trow exeption if error connecting"""
        return mail

    def get_data(self):
        self.mail.select('inbox')
        result, data = self.mail.search(None, '(SUBJECT "test")')
        mail_ids = data
        id_list = mail_ids[0].split()
        print (data)


Save_Inv()



    