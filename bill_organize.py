import imaplib
import email
import os

ORG_EMAIL   = "@gmail.com"
FROM_EMAIL  = "franciscojocosta" + ORG_EMAIL
FROM_PWD    = "K5i2EUH2"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993
'''
Melhorar Git

6 - Funcionar automático
5 - Criar base links para file folders
4 - Adicionar função se folder não existir criar
3 - Logout à conta
2 - Adicionar Segurança à Password
1.2 - Adicionar exceptions e bug-proofing
1 - Limpar Código e Comentar
'''
class Save_Inv():
    
    def __init__(self) -> None:
        print ("Init")
        
    def start(self,rem):
        self.mail = self.connect()
        self.get_att(rem)
    def connect(self):
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        print("Connected")
        """trow exeption if error connecting"""
        return mail

    def get_att(self,rem):

        search_string = '(FROM '+rem+')'

        self.mail.select('inbox')
        _,selected_mails = self.mail.search(None, search_string,'(UNSEEN)')

        for num in selected_mails[0].split():
            typ, data = self.mail.fetch(num, '(RFC822)')

            mail = email.message_from_bytes(data[0][1]) ##Attachment Download starts here...
            for part in mail.walk():
                if part.get_content_maintype() == 'multipart':
                # print part.as_string()
                    continue
                if part.get('Content-Disposition') is None:
                # print part.as_string()
                    continue
                self.save_file(part,rem)
                
    def save_file (self,part,rem):

            fileName = part.get_filename()
            filefolder = rem.split("@",1)[0]
            print(filefolder)

            if "edp" not in filefolder and "agua" not in filefolder:
                filefolder = 'default'

            if bool(fileName):
                filePath = os.path.join("C:\\Users\\franc\\Desktop\\Connect_to_Gmail",filefolder, fileName)

            if not os.path.isfile(filePath):  
                print(fileName)

            if fileName:
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
                print("The file " + fileName + " is saved Successfully")           


F = Save_Inv()
while(1):
    print("Start")
    F.start("faturaedp@edp.pt")
    F.start("aguasdoporto.pt@cgi.com")
    break

