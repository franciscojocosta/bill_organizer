# bill_organizer

----------------------- Bill Organizer -----------------------

Working File - bill_scrapper.py

This program listen to a determined folder for changes in files - this case \Downloads folder - when a new file is sensed the program checks if the file is a water or eletricity bill. 
If yes:
    - Stores the bill in a determined folder based if it is electricity or water bill.
    - Scrappes .pdf file for payment information.
    - Stores the scrapped data in a MySQL database.

Else: Ignores the file

-------------------------------------------------------------

To add a new bill category:
    - Create new "match if (new category)" function on Observer Class
    - Create new scrapping functions for the bill
    - Return "category,id_bill,price,bill_period,entity,reference,limit_date_pay" data to database.
