#!/usr/bin/python3
import sqlite3
import hashlib
from CryptoChat import RSA_decrypt, AES_decrypt, AES_encrypt, RSA_encrypt
from Crypto.Random import random
from Crypto.PublicKey import RSA
from datetime import datetime
from base64 import b64encode, b64decode

alpha = 'abcdefghijklmnopqrstuvxwyz0123456789'
server_db = 'server.db'
def encrypt(plaintext, key=None, mode='RSA'):
    '''Apply the appropriate encryption method to the plaintext
    Return the ciphertext
    '''
    ciphertext = ''
    if mode == 'RSA':
        ciphertext = RSA_encrypt(key, plaintext)
    if mode == 'AES':
        ciphertext = AES_encrypt(key, plaintext)
    return ciphertext

def send(conn, message, key=None):
    '''Send message to client with unique AES key
    '''
    # generate random AES key
    aes_key = ''.join(random.choice(alpha) for i in range(16))

    # encrypt message with this key
    message = encrypt(message, aes_key, 'AES')

    # encrypt the AES key with RSA key
    encrypted_aes_key = encrypt(aes_key, key, 'RSA')

    # concat the RSA-encrypted AES key with the AES-encrypted message
    full_message = encrypted_aes_key + '%' + message

    # prepend with length of message
    length = len('%' + full_message)
    total_length = len(str(length)) + len('%' + full_message)
    full_message = str(total_length) + '%' + full_message

    # send to client
    conn.sendall(full_message.encode())

def recv(conn):
    '''Receive message in chunks. 

    The first chunk will always contain both '%' delimeters. We know this
    because the length of the RSA-encrypted 16 byte AES key
    Return the complete with the length prepend removed
    '''
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
    '''Apply the appropriate encryption method to the ciphertext
    Return the plaintext
    '''
    plaintext = ''
    if mode == 'RSA':
        plaintext = RSA_decrypt(key, ciphertext)
    if mode == 'AES':
        plaintext = AES_decrypt(key, ciphertext)
    return plaintext

def sha_hash(s):
    '''Hash a string using sha512
    Param: the string to hash
    Return the hashed string
    '''
    # get hash of s
    h = hashlib.sha512()
    h.update(s.encode())
    return b64encode(h.digest())

def register(conn, content, client_pub_key = None):
    '''Register or login a user
    Return hashed user name if login successful
    '''
    # unpack message components
    username, password, client_pub = content.split('|')

    # load client RSA key
    client_pub_key = RSA.importKey(b64decode(client_pub))
    print("Received user: {} pass: {}".format(username, password))
    
    # connect to db
    sql_conn = sqlite3.connect(server_db)
    c = sql_conn.cursor()
    
    # check if username already in db
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
        # generate salt
        salt = ''.join(random.choice(alpha) for i in range(12))
        print('salt == {}'.format(salt))
        h_uname = sha_hash(salt + username).decode()
        h_passw = sha_hash(salt + password).decode()

        # add to db
        c.execute('INSERT INTO user (salt, password, username, publickey) \
                VALUES (?, ?, ?, ?)', [salt, h_passw, h_uname, client_pub])
        sql_conn.commit()
        message = "Hey {}! We registered you!".format(username)
    else: # user already registered, and entered correct password
        if authenticated == True:
            message = "Hey {}! We logged you in!".format(username)
        else: # user already registered, but entered incorrect password
            message = "Bad login info!".format(username)
            h_uname = None

    send(conn, message, client_pub_key)
    print("sent response")
    return h_uname, client_pub
    

def send_message(conn, content, client_pub_key):
    '''Load a message into message table on behalf of client
    These messages will reside in db until retrieved by target user
    '''
    # get message components
    userto, msg_content = content.split('|')
    print("sending message to {}: '{}'".format(userto, msg_content))

    # connect to db
    sql_conn = sqlite3.connect(server_db)
    c = sql_conn.cursor()

    # search for user, grabbing hashed username if they exist
    c.execute('SELECT salt, username, password FROM user')
    h_userto = None
    for row in c:
        if sha_hash(str(row[0]) + userto).decode() == str(row[1]):
            h_userto = str(row[1])

    # if user was found, store message for delivery
    if h_userto: 
        timestamp = str(datetime.now())
        c.execute('INSERT INTO message (message_date, target_user, content) \
                VALUES (?, ?, ?)', [timestamp, h_userto, msg_content])
        sql_conn.commit()
        message = "message sent!"
    else:
        message = "invalid target user!"

    # send result to client
    send(conn, message, client_pub_key)
    
def recv_message(conn, user, client_pub_key):
    '''Search message db for undelivered messages addressed to user
    If they exist, send to recipient
    '''

    # connect to db
    sql_conn = sqlite3.connect(server_db)
    c = sql_conn.cursor()
    
    # find hashed username
    c.execute('SELECT salt, username, password FROM user')
    h_userto = None
    for row in c:
        if sha_hash(str(row[0]) + user).decode() == str(row[1]):
            h_userto = str(row[1])

    # search for messags
    print("finding messages for user {}".format(h_userto))
    c.execute('SELECT rowid, target_user, content, message_date FROM message WHERE target_user = ? AND delivered = 0', [h_userto])
    messages = ''
    message_ids = []
    message_time = []
    for row in c:
        print("sending message {} to {}".format(str(row[2]), str(row[1])))
        messages += str(row[2]) + '|'
        message_ids.append(row[0])
        message_time.append(row[3])
    message = messages[:-1]
    if message == '':
        message = "You have no new messages"
    
    # mark messages as delivered
    for msg_id in message_time:
        #print(msg_id)
        #TODO set delivered = 1 in database
        c.execute('UPDATE message SET delivered = ? WHERE message_date = ?', [bin(1),msg_id])
        sql_conn.commit()
        #pass

    # send to client
    send(conn, message, client_pub_key)





