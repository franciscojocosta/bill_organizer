import mysql.connector
'''
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="root"
)

mycursor = mydb.cursor()

mycursor.execute("SHOW DATABASES")

for x in mycursor:
  print(x)

'''

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="root",
  database="bills"
)

mycursor = mydb.cursor()
mycursor.execute("SHOW columns FROM bills")

for column in mycursor.fetchall():
    print(column[0])
val = '122312'
query = "INSERT INTO bills (tipo,id_fatura,price,periodo_fatura,entidade,referencia,data_limite ) VALUES (%s,%s,32,%s,3324,543,'21/05/22')"
record = val,val,val
mycursor.execute(query,record)


for x in mycursor:
  print(x)
  print ("\n")

mydb.commit()