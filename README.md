# bill_organizer


Working File - bill_scrapper.py

This program listens to a determined folder for changes in files - this case \Downloads folder - when a new file is sensed the program checks if the file is a water or eletricity bill. 

If yes:
- Stores the bill in a determined folder based if it is electricity or water bill.
- Scrappes .pdf file for payment information.
- Stores the scrapped data in a MySQL database.

Else: Ignores the file

**************************************************                 **************************************************

To add a new bill category:
- Create new "match if (new category)" function on Observer Class
- Create new scrapping functions for the bill
- Return "category,id_bill,price,bill_period,entity,reference,limit_date_pay" data to database.

This project was originally made to detect new bills via e-mail on gmail account and download the attachment, but with new google restriction on unsecure connection, scope of the project was changed. Anyhow, on \dev there are still scripts made for that functionality (connect_to_gmail.py, save_att.py,..).
