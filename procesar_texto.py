import sqlite3
import re

connection = sqlite3.connect("channels.db")
cursor = connection.cursor()
cursor.execute('''
select * from dataset_individual LIMIT 100;
''')
resultado = cursor.fetchall()
cursor.close()
connection.close()










for x in range(10):
    print(resultado[x][6])




