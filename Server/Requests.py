#!/usr/bin/python3
from CryptoChat import RSA_decrypt
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
        print(chunk_count, firstchunk)
        received = len(firstchunk)
        content = ''
        length, chunk = firstchunk.split('%')
        content += chunk
        while received < int(length):
            nextchunk = conn.recv(1024).decode()
            received += len(nextchunk)
            content += nextchunk
        return content
    return None

def decrypt(ciphertext, key=None, mode='RSA'):
    plaintext = ''
    if mode == 'RSA':
        plaintext= RSA_decrypt(key, ciphertext)
    return plaintext

def register(conn, content):
    #TODO generate salt, hash salt + name, hash salt + pwd, store in db 
    print("register!")
    username, password = content.split('|')
#    username, password, client_pub = content.split('|')
    #print("client pub = {}".format(client_pub))
    print("Received user: {} pass: {}".format(username, password))
    message = "sup {} we registered you!".format(username)
    send(conn, message)
    print("sent response")
    

def send_message(conn, content):
    #TODO store in message db
    pass

def recv_message(conn, content):
    #TODO search message db for undelivered messages for recipient
    #       if they exist, send to recipient
    pass
