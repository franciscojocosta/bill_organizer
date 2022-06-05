import imaplib
import email
from typing_extensions import Self
import os

ORG_EMAIL   = "@gmail.com"
FROM_EMAIL  = "franciscojocosta" + ORG_EMAIL
FROM_PWD    = "K5i2EUH2"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993

class Save_Inv:
    
    def __init__(self) -> None:
        print ("Init")
        self.mail = self.connect()
        self.read_email()
    
    def connect(self):
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        print("Connected")
        """trow exeption if error connecting"""
        return mail

    def read_email(self):
        self.mail.select('inbox')
        _,selected_mails = self.mail.search(None, '(FROM "franciscojocosta@gmail.com")')
        
        print("Total Messages from franciscojocosta@gmail.com:" , len(selected_mails[0].split()))
        for msgId in selected_mails[0].split():
            
            typ, messageParts = self.mail.fetch(msgId , '(RFC822)')
            if typ != 'OK':
                print ('Error fetching mail.')
                raise
            
            emailBody = messageParts[0][1]
    
            mail = email.message_from_string(emailBody)
            for part in mail.walk():
                if part.get_content_maintype() == 'multipart':
                    # print part.as_string()
                    
                    continue
                if part.get('Content-Disposition') is None:
                    # print part.as_string()
                    continue
                
                fileName = part.get_filename()

                if bool(fileName):
                    filePath = "C:/Users/franc/Desktop/Connect_to_Gmail"
                    
                    if not os.path.isfile(filePath) :
                        print (fileName)
                        fp = open(filePath, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()
            


Save_Inv()