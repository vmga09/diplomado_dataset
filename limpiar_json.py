import sys
import json
import sqlite3
import os
import re


def clean_text(text):
    """Limpia el texto"""
    text_with_spaces = text.replace('\n', ' ')
    text_with_spaces = text_with_spaces.replace('\t', ' ')
    return re.sub(r'[^a-zA-Z0-9 @?]', '', text_with_spaces)
    



def create_table():
    """Creacion de la tabla si no existe"""
    connection = sqlite3.connect("channels.db")
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
        channel_length_text integer,
        channel_file TEXT,
        channel_length_file integer,
        channel_etiqueta TEXT
    )   
    ''')
    connection.commit()
    connection.close()

create_table()

def insertar(lista):
    """Insertar"""
    connection = sqlite3.connect("channels.db")
    cursor = connection.cursor()
    
    #Inserta los valores
    query = """INSERT INTO dataset_individual (
    channel_id, 
    channel_name, 
    channel_title, 
    channel_description, 
    channel_url, 
    channel_text,
    channel_length_text,
    channel_file,
    channel_length_file,
    channel_etiqueta 
    ) VALUES (?, ?, ?,?,?,?,?,?,?,?)"""
    cursor.executemany(query,lista)
    connection.commit()
    connection.close()



with open(os.path.join('dataset/',sys.argv[1]),encoding="utf8") as f:
    data = json.load(f)
    channel_id = data['channel_id']
    channel_name = data['channel_name']
    channel_title = data['channel_title']
    channel_description = data['channel_description']
    channel_url = data['channel_url']
    channel_etiqueta = data['etiqueta']
    channel_message = list(data['messages'])
    
    #print(channel_id, channel_name, channel_title, channel_description, channel_url, channel_etiqueta, channel_message)
    datos = []
    for _ in channel_message:
        text_length = len(_['text'])
        file_length = len(_['file'])
        clean_texto = clean_text(_['text'])
        if text_length < 10 and file_length < 1:
            continue
        if file_length < 1:
            channel_etiqueta = 'no'
        else: 
            channel_etiqueta = 'yes'
        info = (channel_id, 
                channel_name, 
                channel_title, 
                channel_description, 
                channel_url,
                clean_texto,
                text_length,
                _['file'],
                file_length,
                channel_etiqueta)
        datos.append(info)
    
     #print(channel_id, channel_name, channel_title, channel_description, channel_url, channel_etiqueta, _['text'],_['file'])
    
    insertar(datos)