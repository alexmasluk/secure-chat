from CryptoChat import RSA_encrypt, AES_encrypt
from Crypto.Cipher import AES
from Crypto.Random import random
from base64 import b64encode, b64decode

def recv(sock):
    firstchunk = sock.recv(1024).decode()
    received = len(firstchunk)
    content = ''
    length, chunk = firstchunk.split('%')
    content += chunk
    while received < int(length):
        nextchunk = sock.recv(1024).decode()
        received += len(nextchunk)
        content += nextchunk
    return content

def encrypt(plaintext, key=None, mode='RSA'):
    ciphertext = ''
    if mode == 'RSA':
        ciphertext = RSA_encrypt(key, plaintext)
    if mode == 'AES':
        ciphertext = AES_encrypt(key, plaintext)
    
    return ciphertext

def send(sock, message, key=None):
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
    name = input("Username: ")
    passwd = input("Password: ")
    client_pub = b64encode(client_key.publickey().exportKey('PEM')).decode()
    print("attempting to register '{}'".format(name))
    message = 'reg#' + name + '|' + passwd + '|' + client_pub

    print("sending")
    send(sock, message, server_key)
    print("waiting response")
    response = recv(sock)
    print("response received: {}".format(response))


def recv_message():
    pass

def send_message():
    pass
