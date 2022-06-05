import imaplib
import email
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
        for num in selected_mails[0].split():
            _, data = self.mail.fetch(num , '(RFC822)')
            _, bytes_data = data[0]
            
            #convert the byte data to message
            email_message = email.message_from_bytes(bytes_data)
            print("\n===========================================")

            #access data
            print("Subject: ",email_message["subject"])
            print("To:", email_message["to"])
            print("From: ",email_message["from"])
            print("Date: ",email_message["date"])
            for part in email_message.walk():
                if part.get_content_type()=="text/plain" or part.get_content_type()=="text/html":
                    message = part.get_payload(decode=True)
                    print("Message: \n", message.decode())
                    print("==========================================\n")
                    break


Save_Inv()
