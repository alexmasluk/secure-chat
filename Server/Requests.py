#!/usr/bin/python3
import sqlite3
import uuid
import hashlib
from CryptoChat import RSA_decrypt, AES_decrypt
from Crypto.Random import random
from base64 import b64encode, b64decode

alpha = 'abcdefghijklmnopqrstuvxwyz0123456789'
server_db = 'server.db'
def encrypt(plaintext, key=None, mode='RSA'):
    ciphertext = ''
    if mode == 'RSA':
        ciphertext = RSA_encrypt(key, plaintext)
    if mode == 'AES':
        ciphertext = AES_encrypt(key, plaintext)
    return ciphertext

def send(conn, message, key=None):
    aes_key = ''.join(random.choice(alpha) for i in range(16))
    message = encrypt(message, aes_key, 'AES')
    encrypted_aes_key = encrypt(aes_key, key)
    full_message = encrypted_aes_key + '%' + message
    length = len('%' + full_message)
    total_length = len(str(length)) + len('%' + full_message)
    full message = str(total_length) + '%' + full_message

    conn.sendall(full_message.encode())

def recv(conn):
    firstchunk = conn.recv(1024).decode()
    chunk_count = 0
    if firstchunk:
        chunk_count += 1
        #print(chunk_count, firstchunk)
        received = len(firstchunk)
        content = ''
        length, keypart, message = firstchunk.split('%')
        content += keypart + '%' + message
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
    '''Register or login a user
    Return hashed user name if login successful
    '''
    # unpack relevant data
    username, password, client_pub = content.split('|')
    print("Received user: {} pass: {}".format(username, password))
    #print("client pub = {}".format(b64decode(client_pub)))
    
    # generate salt
    salt = ''.join(random.choice(alpha) for i in range(12))
    print('salt == {}'.format(salt))

    # check if username already in db
    sql_conn = sqlite3.connect(server_db)
    c = sql_conn.cursor()
    c.execute('SELECT salt, username, password FROM user')
    already_exists = False
    authenticated = False
    h_uname = None
    for row in c:
        if sha_hash(str(row[0]) + username).decode() == str(row[1]):
            already_exists = True
            # authenticated with password
            if sha_hash(str(row[0]) + password).decode() == str(row[2]):
                authenticated = True
                h_uname = str(row[1])

    # if doesn't exist, add to db
    if already_exists == False:
        h_uname = sha_hash(salt + username).decode()
        h_passw = sha_hash(salt + password).decode()
        uid = str(uuid.uuid4())
        c.execute('INSERT INTO user (user_id, salt, password, username, publickey) \
                VALUES (?, ?, ?, ?, ?)', [uid, salt, h_passw, h_uname, client_pub])
        sql_conn.commit()
        message = "Hey {}! We registered you!".format(username)
        logged_in_user = h_uname
    else:
        if authenticated == True:
            message = "Hey {}! We logged you in!".format(username)
        else:
            message = "Bad login info!".format(username)
            h_uname = None

    send(conn, message)
    print("sent response")
    return h_uname
    

def send_message(conn, content):
    #TODO store in message db
    pass

def recv_message(conn, content):
    #TODO search message db for undelivered messages for recipient
    #       if they exist, send to recipient
    pass
