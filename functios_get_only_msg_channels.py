
import sys
from telethon.sync import TelegramClient, errors, types
from telethon.sessions import StringSession
from telethon.tl.types import Channel, Chat, User
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon import functions, types
import query.query_sql as query_sql
import random
import json
import re
import sqlite3

telefono = "+56920982790"

#Genera diccionario con mensaje 
def messages_info(msg):
    message = {}
    message['id']=str(msg.id)
    message['id_channel']=str(msg.peer_id.channel_id)
    message['date']=msg.date.strftime("%Y-%m-%d %X")
    message['message']=str(msg.message)
    return message



def register_enlaces(data):
    patron_canal = r't\.me/\w+'
    enlaces = []
    for _ in data:
        message = _[1]
        links = re.findall(patron_canal, message)
        enlaces = enlaces + links

    connection = sqlite3.connect("channels.db")
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS telegram_links (
        id INTEGER PRIMARY KEY,
        enlaces TEXT UNIQUE
    )
    ''')
    new_enlaces = list(set(enlaces))
    for _ in new_enlaces:
        cursor.execute("SELECT * from list_channels where channel_name = ?",(f't.me/{_}',))
        result = cursor.fetchall()
        if len(result) > 0:
            registrado = 'yes'   
        else:
            registrado = 'no'
        cursor.execute("INSERT OR IGNORE INTO telegram_links (enlaces,registrado) VALUES (?,?)",(str(_),registrado))
        connection.commit()
    connection.close()






#Funcion que retorna un arreglo diccionarios 
def get_old_messages(url_channel):
    output = []
    phone = telefono
    api = query_sql.find_client_telegram(phone)
    api_id = api[0][1]
    api_hash = api[0][2]
    #num_message = 20
    num_message = 2000
    clientes = query_sql.get_all_session_by_phone(phone)
    cliente = random.choice(clientes)


    client = TelegramClient(StringSession(cliente), api_id, api_hash).start()
    channel = url_channel
    try:     
        last_messages = client.get_messages(channel, limit=num_message, reverse=False)
        #enlaces = client.get_messages(channel,filter=types.InputMessagesFilterUrl())
    # Si aparece este error retorna lista sin valores
    #except errors.FloodWaitError as e:
    except Exception as e:
        client.disconnect()
        output.append({"message": e.args[0]})
        print(output)

        #sys.exit(output)
    else:
        for item in last_messages:
            result = ''
            if item.document:
                try:
                   result=item.document.attributes[0].file_name
                except:
                    result =''       
            message = messages_info(item)
            info = (message['date'],message['message'],result)
            output.append(info)
        client.disconnect()
    return output


   


def list_channel():
    connection = sqlite3.connect("channels.db")
    cursor = connection.cursor()
    cursor.execute("SELECT enlaces from telegram_links")
    result = cursor.fetchall()
    result = [ _[0] for _ in result ]
    connection.close()
    return result
    




def buscar(id):
    connection = sqlite3.connect("channels.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * from list_channels where channel_id = ?",(id,))
    result = cursor.fetchall()
    connection.close()
    return result



def insertar(chat_name,lista):
    connection = sqlite3.connect("channels.db")
    cursor = connection.cursor()
    # Crea la tabla si no existe
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {chat_name} (
        id INTEGER PRIMARY KEY,
        message_date TEXT,
        message_text TEXT,
        message_file TEXT                      
    )
    ''')
    connection.commit()
    



    #Inserta los valores
    query = f"INSERT INTO {chat_name} (message_date, message_text, message_file) VALUES (?, ?, ?)"
    cursor.executemany(query,lista)
    connection.commit()
    connection.close()




if __name__ == '__main__':
    #channels_list = list_channel()
    #print(f"Lista ce canales: {len(channels_list)}")
    #for _ in channels_list:
    #    chat_name = _[5:]
    last_messages = get_old_messages(sys.argv[1])
    if len(last_messages) > 1:
        register_enlaces(last_messages)
        insertar(sys.argv[1][5:],last_messages)
    else:
        print(f"{sys.argv[1]} no es canal válido")



    