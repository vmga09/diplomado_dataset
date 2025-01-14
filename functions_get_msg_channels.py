
import sys
from telethon.sync import TelegramClient, errors, types
from telethon.sessions import StringSession
from telethon.tl.types import Channel, Chat, User
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon import functions, types
#import query.query_sql as query_sql
import random
import json
import re
import sqlite3



telefono = "+56920982790"
api_id = "29039967"
api_hash = "c137731948c2a91a07e1430bd8733d8e"

clientes = [
    "1AZWarzoBu4aSvYgjrDl3pAghWLk_rIVgdzCT2CBgzXvJiM2_tHg7k4z-I72hJ1JRJTiL7HuUJv4ew6_raaqnxcomQfH8JMbCAzXaEYogRnE5l2o-RrtWS6oqf7TNpf_pDP4O2a1UbVtRe5Fw3c5QLFOa1eaL4iblNuAeou-5u-PlT3WIBFJDYLqnKlDtrR16rnXeJAqJObbxKo2mqgNQHk0RtrHKQphXDGePuuFV3_LGP1olH3TZCffGTjxI0_YQrrLuqehFkEOXllKrlfIsclszEtPVScwPXA2T8VYsCHscvARjYQWLB7OATN-7_QtfeE4-e7oS1pZ8Drwn4XpVMjWODHKi_S8=",
    "1AZWarzoBu6CRsDLG2HiQwdXp3BEWULY9KYaZtFcAOyUwAQ0GAlQkjBNaMMgMz2zlmy9NCV62zAz7_3DD8uyJ-vwSReYy3WoFJbqYdTTTTdB_I2ci0tzqTITbgb3Y7jDBcGQBuHB0vl_DWD_BHTjjddBlfxy3RggxAvwq18dln1wncKFqMlKAzltTEzp8Tcd7StrtLpQDqq_JpPFU-Gr6N5sDj6Oiq07J9KlH_N7_9DBpUAF7xfhvH0MnzTTRPLd5QwoFyhGfO4ckp2gu3vJL_Xl-EQi_x-ftnBRTt0vscVmxw18GxVA3jpDaotVrH1Bqw_m5XyzFqJ7i3jSmRUy8hY0gzKWWE_s=",
    "1AZWarzoBu7GC2fNiFzfurlyVbvlezEBmgDUN0rLOXGbB_n8oPtqtK04u-vZFo9MJhiPYDVRXRwYRCo6rHIhtcJRucOnZe2D9jgEBl9PKKyLiP5k3nebH-Os5Cqv4sJL1Pt8bdT6UF9PCa7OiwCTLOOmvwTqfG6WktKX_mLCygwUF1FrWLY-1mVuVLXLeyQyOYYcnznyCaDThTJgnZ7f9iDliaGmDbXYqKfrFV00wPyyFkCZLPmLI3ngRVRM7Z6YxOcvkaPuMXmfulJeYtpJfGDakqhse_rBR5ihW_mEvXb4UqiNHXbeZ_aqjGA5t_LjnnqxrbOUwKT5OoA2jpkdGYPpBCAOrHcM=",
    "1AZWarzoBuxW_7_a6_4sEtkoLT3bRfRFwKtZjQmWRqtlJtDRVwSPLb83CEnfMpZXPJoutbHqeDTcbGCh_vavWBRpw1J4NctMDsekxAi4K_7f0gG7uAZLACmD1Zy6ln81OJ9u5YsrpUBxgiu7H_TY75gbOhFoaPLrNCqGP2VAjrqLziRpKMtorarLSbTs0F7LCE5iSaRE7BBRah8SUM-D_cG2cXQvPH9qrDkrslPnsE1V501C3Tl02lu7IDX5bLe_ZqAjxkWzmiwNQGM6oaQNg85SMieDfLOUHjNZjP-7CwxVQugbQoJw14BKYeOwEaECWoj6nZJgA3F1qjzX38dwiij3gQT3aOJg=",
    "1AZWarzoBu7ev0cE9B929hUE8H4RUr5lCT6WM-b0wBIJIUlOGPJ7BOchg3UwgBpoYKaxsxXGNtddW4WmmYqFJBCnYV5mwbHXvNrQFkb-lnJmRLiyxfshqSLiLRMz4MS7pZdayTQM_MHN4fyppvVGV3ie33RCFghe6pVnRZV6MSOOy9QsdMRSD--71BUzx1rKnG-kXgRBWo71YawSXRbhoqSGkIxx4OaWAtP5nAt96YtvUxb_bSsu2JddbgertDpvG0kAwh5uD6yWJ1tcDYd_E5lhXyNoqWI2i5390jTjqOmsCGnjkPPmlOeVC3FgY_AEM1NZBEUuXfVTdNWUe7H4oqX0assajN9Q="
]




#Genera diccionario con mensaje 
def messages_info(msg):
    message = {}
    message['id']=str(msg.id)
    message['id_channel']=str(msg.peer_id.channel_id)
    message['date']=msg.date.strftime("%Y-%m-%d %X")
    message['message']=str(msg.message)
    return message


def register_enlaces(data,channel):
    patron_canal = r't\.me/\w+'
    channel_name = channel['channel_name']
    channel_id = channel['channel_id']
    enlaces = []
    for _ in data:
        message = _['message']
        links = re.findall(patron_canal, message)
        enlaces = enlaces + links
    
    
    connection = sqlite3.connect("channels.db")
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS enlaces (
        id INTEGER PRIMARY KEY,
        channel_id TEXT UNIQUE,
        channel_name TEXT,
        enlaces TEXT
    )
    ''')
    new_enlaces = list(set(enlaces)) 
    print(channel_id,channel_name,new_enlaces)
    cursor.execute("INSERT OR IGNORE INTO enlaces (channel_id,channel_name,enlaces) VALUES (?,?,?)",(str(channel_id),channel_name,str(new_enlaces)))
    connection.commit()
    connection.close()



#Funcion que retorna un arreglo diccionarios 
def get_old_messages(url_channel):
    output = []
    #phone = telefono
    #api = query_sql.find_client_telegram(phone)
    #api_id = api_id
    #api_hash = api[0][2]
    #num_message = 20
    num_message = 2000
    #clientes = query_sql.get_all_session_by_phone(phone)
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
        sys.exit(output)
    else:
        for item in last_messages:
            info = {}
            result = ''
            if item.document:
                try:
                   result=item.document.attributes[0].file_name
                except:
                    result =''       
            message = messages_info(item)
            info['fecha'] = message['date']
            info['text'] = message['message']
            info['file'] = result
            if len(info['text']) < 10 and len(info['file']) < 1:
                continue
            else:
                output.append(info)
        client.disconnect()
    return output



def get_entity_telegram(url):
    channel = {}
    phone = telefono
    api = query_sql.find_client_telegram(phone)
    api_id = api[0][1]
    api_hash = api[0][2]
    clientes = query_sql.get_all_session_by_phone(phone)
    cliente = random.choice(clientes)
    client = TelegramClient(StringSession(cliente), api_id, api_hash).start()
    try:
        my_entity = client.get_entity(url)
        my_channel = client(GetFullChannelRequest(channel=url))
    except Exception as e:
        channel['channel_status'] = False
        channel['channel_error'] = e.args[0]
    else:
        if isinstance(my_entity, User):  # Check if it's a User (private chat)
            channel['channel_type'] = "Private Chat"
        elif isinstance(my_entity, Channel):  # Check if it's a Channel
            channel['channel_type'] = "Channel"
        elif isinstance(my_entity, Chat):  # Check if it's a Chat (group)
            channel['channel_type'] = "Group"
        else:
            channel['channel_type'] = "Unknown"  
        #channel['channel_status'] = True
        channel['channel_id'] = my_channel.full_chat.id
        print('id channel : ',my_channel.full_chat.id)
        channel['channel_name'] = my_entity.username
        channel['channel_url'] = "t.me/"+str(my_entity.username)
        channel['channel_title'] = my_entity.title
        channel['channel_description'] = my_channel.full_chat.about
        channel['channel_members'] = my_channel.full_chat.participants_count
        channel['channel_online']= my_channel.full_chat.online_count if my_channel.full_chat.online_count is not None else 0
        channel['channel_error'] = "None"  
    client.disconnect()        
    return channel    


def telegram_codigo(url):
    phone = telefono
    api = query_sql.find_client_telegram(phone)
    api_id = api[0][1]
    api_hash = api[0][2]
    clientes = query_sql.get_all_session_by_phone(phone)
    cliente = random.choice(clientes)
    client = TelegramClient(StringSession(cliente), api_id, api_hash).start()
    result = client(functions.messages.ImportChatInviteRequest(
        hash=url[6:]
    ))
    print(result.chats)
    print(result.stringify())
    client.disconnect() 


def buscar(id):
    connection = sqlite3.connect("channels.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * from list_channels where channel_id = ?",(id,))
    result = cursor.fetchall()
    connection.close()
    return result


def insert_data(channel_id,channel_name,channel_label):
    connection = sqlite3.connect("channels.db")
    cursor = connection.cursor()
    cursor.execute("""
    INSERT OR IGNORE INTO list_channels(channel_id,channel_name,channel_label) VALUES (?,?,?) 
""",(channel_id,channel_name,channel_label))
    connection.commit()
    connection.close()



if __name__ == '__main__':
    archivo = f"dataset/{sys.argv[1]}_datos.json"
    last_messages = get_old_messages(sys.argv[1])
    channel_info = get_entity_telegram(sys.argv[1])
    channel_info['messages'] = last_messages
    channel_info['etiqueta'] = sys.argv[2]
    print(channel_info['channel_id'])
    #register_enlaces(last_messages,channel_info)


    if len(buscar(int(channel_info['channel_id']))) > 0:
        print(f"{channel_info['channel_id']} - {channel_info['channel_name']} ya esta registrado")
         
    else:

        if sys.argv[3] == 'w':
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump(channel_info, f, ensure_ascii=False, indent=4)
        else:
            for elemen in last_messages:
                print(elemen)
        insert_data(channel_id=int(channel_info['channel_id']),channel_name=channel_info['channel_name'],channel_label=sys.argv[2])
        


    
