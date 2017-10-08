#!/usr/bin/python3
import sqlite3
import uuid
import hashlib
from CryptoChat import RSA_decrypt, AES_decrypt
from Crypto.Random import random
from base64 import b64encode, b64decode

alpha = 'abcdefghijklmnopqrstuvxwyz0123456789'
server_db = 'server.db'
def send(conn, message):
    length = len('%' + message)
    total_length = len(str(length)) + len('%' + message)
    message = str(total_length) + '%' + message
    conn.sendall(message.encode())

def recv(conn):
    firstchunk = conn.recv(1024).decode()
    chunk_count = 0
    if firstchunk:
        chunk_count += 1
        #print(chunk_count, firstchunk)
        received = len(firstchunk)
        content = ''
        length, keypart, message = firstchunk.split('%')
        content += keypart + '%' +  message
        while received < int(length):
            nextchunk = conn.recv(1024).decode()
            received += len(nextchunk)
            content += nextchunk
        return content
    return None

def decrypt(ciphertext, key=None, mode='RSA'):
    plaintext = ''
    if mode == 'RSA':
        plaintext = RSA_decrypt(key, ciphertext)
    if mode == 'AES':
        plaintext = AES_decrypt(key, ciphertext)
    return plaintext

def sha_hash(s):
    # get hash of s
    h = hashlib.sha512()
    h.update(s.encode())
    return b64encode(h.digest())

def register(conn, content):
    # unpack relevant data
    username, password, client_pub = content.split('|')
    print("Received user: {} pass: {}".format(username, password))
    #print("client pub = {}".format(b64decode(client_pub)))
    
    # generate salt
    salt = ''.join(random.choice(alpha) for i in range(12))
    print('salt == {}'.format(salt))

    success = False
    #TODO check if username already in db
    sql_conn = sqlite3.connect(server_db)
    c = sql_conn.cursor()
    c.execute('SELECT salt, username FROM user')
    already_exists = False
    for row in c:
        print('hash == {} str_value == {}'.format(sha_hash(str(row[0]) + username), str(row[1])))
        if sha_hash(str(row[0]) + username) == str(row[1]):
            already_exists = True

    #TODO if doesn't exist, add to db
    if already_exists == False:
        success = True
        uid = str(uuid.uuid4())
        h_uname = sha_hash(salt + username)
        h_passw = sha_hash(salt + username)
        c.execute('INSERT INTO user (user_id, salt, password, username, publickey) \
                VALUES (?, ?, ?, ?, ?)', [uid, salt, h_passw, h_uname, client_pub])
        sql_conn.commit()


    if success == True:
        message = "sup {} we registered you!".format(username)
    else:
        message = "dude you already registered..."
    send(conn, message)
    print("sent response")
    

def send_message(conn, content):
    #TODO store in message db
    pass

def recv_message(conn, content):
    #TODO search message db for undelivered messages for recipient
    #       if they exist, send to recipient
    pass
