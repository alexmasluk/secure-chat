from CryptoChat import RSA_encrypt, AES_encrypt, RSA_decrypt, AES_decrypt
from Crypto.Cipher import AES
from Crypto.Random import random
from datetime import datetime
from base64 import b64encode, b64decode
import sqlite3
import hashlib

client_db = 'client.db'

def recv(sock):
    '''receive data from server
    '''
    firstchunk = sock.recv(1024).decode()
    chunk_count = 0
    if firstchunk:
        received = len(firstchunk)
        content = ''
        length, keypart, message = firstchunk.split('%')
        content += keypart + '%' + message
        while received < int(length):
            nextchunk = sock.recv(1024).decode()
            received += len(nextchunk)
            content += nextchunk
        return content
    return None

def decrypt(ciphertext, key=None, mode='RSA'):
    '''Apply appropriate encryption method to ciphertext
    Return the plaintext
    '''
    plaintext = ''
    if mode == 'RSA':
        plaintext = RSA_decrypt(key, ciphertext)
    if mode == 'AES':
        plaintext = AES_decrypt(key, ciphertext)
    return plaintext

def encrypt(plaintext, key=None, mode='RSA'):
    '''Apply appropriate encryption method to the plaintext
    Return the ciphertext
    '''
    ciphertext = ''
    if mode == 'RSA':
        ciphertext = RSA_encrypt(key, plaintext)
    if mode == 'AES':
        ciphertext = AES_encrypt(key, plaintext)
    
    return ciphertext

def send(sock, message, key=None):
    '''Send message to server
    '''
    # generate random AES key 
    aes_key = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz01234567890') for i in range(16))

    # encrypt message using AES key
    message = encrypt(message, aes_key, 'AES')
    
    # encrypt key using server public RSA key
    encrypted_aes_key = encrypt(aes_key, key)

    # message format: message_length%encrypted_AES_key%message
    full_message = encrypted_aes_key + '%' + message
    length = len('%' + full_message)
    total_length = len(str(length)) + len('%' + full_message)
    full_message = str(total_length) + '%' + full_message

    # send message to server
    sock.sendall(full_message.encode())


def register(sock,server_key=None,client_key=None,mode=None): 
    '''register or login
    '''
    name = input("Username: ")
    passwd = input("Password: ")
    client_pub = b64encode(client_key.publickey().exportKey('PEM')).decode()
    message = 'reg#' + name + '|' + passwd + '|' + client_pub
    send(sock, message, server_key)
    return name


def list_contacts():
    c = sqlite3.connect(client_db).cursor()
    c.execute('SELECT username FROM contact')
    print("Contacts")
    for row in c:
        print("[{}]".format(str(row[0])))

def sha_hash(s):
    '''Hash a string using sha512
    Param: the string to hash
    Return the hashed string
    '''
    # get hash of s
    h = hashlib.sha512()
    h.update(s.encode())
    return b64encode(h.digest())


def otk_hash(k, messages=None):
    if messages == None:
        return k
    if len(messages) == 1:
	    k = sha_hash(k) + sha_hash(messages[0])
    if len(messages) == 2:
	    k = sha_hash(k) + sha_hash(messages[0] + messages[1])
    if len(messages) == 3:
	    k = sha_hash(k + messages[0]) + sha_hash(messages[1] + messages[2])
    return k

def one_time_key(user, key, target):
    out =[]
    c = sqlite3.connect(client_db).cursor()
    n = "SELECT content FROM message WHERE \
            (target_user = '" + user + "' AND source_user = '" + target + "') \
            OR (target_user = '" + target + "' AND source_user = '" + user + "') \
            ORDER BY message_time DESC LIMIT 3" 

    for row in c:
        out.append(row[0])

    string_key = otk_hash(key, out)
    #print(type(string_key))
    #print(type(str.encode(string_key))+ " " + string_key)
    key_out = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz01234567890') for i in range(16))
    #print(size(key_out))
    return key_out

def diffie_hellman():
    pass
    return 0

def send_message(sock, server_key, client_key, username):
    list_contacts()
    target_user = input("Send to: ")
    message     = input("Message: ")


    sql_conn = sqlite3.connect(client_db)
    c = sql_conn.cursor()
    # check to see if user already in contacts 
    '''
    sql_conn = sqlite3.connect(client_db)
    c = sql_conn.cursor()
    c.execute('SELECT username, shared_key FROM contact')
    found = False
    shared_key = None
    for row in c:
        if str(row[0]) == target_user:
            found = True
            shared_key = str(row[1])

    if not found:
        # need a key exchange
        shared_key = diffie_hellman()
        c.execute('INSERT INTO contact (username, shared_key) \
                VALUES (?, ?)', [target_user, shared_key])
    '''
	
    shared_key = diffie_hellman()
    date = str(datetime.now())
    otk = one_time_key(username, shared_key, target_user)
    c.execute('INSERT INTO message (message_time, content, source_user, target_user) \
            VALUES (?, ?, ?, ?)', [date, message, username, target_user]) 
    message = encrypt(message, otk, 'AES')

    
    

    sql_conn.commit()
    message = 'snd#' + target_user + '|' + username +": "+  message 
    send(sock, message, server_key)
    print("waiting response")

def recv_message(sock, server_key, client_key, username):
    message = 'rcv#' + username
    send(sock, message, server_key) 

def decodeMessage(username, message, target):

    shared_key = 0
    target_user = target
    otk = one_time_key(username, shared_key, target_user)
    #message = message.decode('utf-8')
    message = decrypt(message, otk, 'AES')
    return message

    
    
    
