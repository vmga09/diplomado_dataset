import sqlite3
import re
from emoji_patterns import EMOJI_PATTERN

connection = sqlite3.connect("channels.db")
cursor = connection.cursor()
cursor.execute('''
select
 channel_id,
 channel_name,
 channel_title,
 channel_description,
 channel_url,
 channel_text,
 channel_file,
 channel_etiqueta
 from dataset_individual;
''')
resultado = cursor.fetchall()
cursor.close()
connection.close()

def create_new_db():
    connection = sqlite3.connect("dataset.db")
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dataset_individual (
        id INTEGER PRIMARY KEY,
        channel_id INTEGER,
        channel_name TEXT,
        channel_title TEXT,
        channel_description TEXT,
        channel_url TEXT,
        channel_text TEXT,
        channel_file TEXT,
        channel_etiqueta TEXT
    )   
    ''')
    connection.commit()
    connection.close()

create_new_db()


def clean_text(text):
    # Eliminar emojis usando expresiones regulares
    emoji_pattern = re.compile(EMOJI_PATTERN, flags=re.UNICODE)
    
    # Eliminar emojis
    text = emoji_pattern.sub('', text)
    
    # Remover hashtags y menciones
    #text = re.sub(r'#\w+', '', text)  # Remover hashtags
    text = re.sub(r'@\w+', '', text)  # Remover menciones

    # Reemplazar múltiples espacios en blanco por uno solo
    #text = re.sub(r'\s+', ' ', text)
    text = ' '.join(text.split())
    
    # Eliminar espacios al inicio y final
    text = text.strip()
    
    return text


new_list = []
for x in resultado:
    temp_x = list(x)
    temp_x[5] = clean_text(temp_x[5])
    info = tuple(temp_x)
    new_list.append(info)


def insertar(lista):
    """Insertar"""
    connection = sqlite3.connect("dataset.db")
    cursor = connection.cursor()
    
    #Inserta los valores
    query = """INSERT INTO dataset_individual (
    channel_id, 
    channel_name, 
    channel_title, 
    channel_description, 
    channel_url, 
    channel_text,
    channel_file,
    channel_etiqueta 
    ) VALUES (?, ?, ?,?,?,?,?,?)"""
    cursor.executemany(query,lista)
    connection.commit()
    connection.close()


insertar(new_list)

