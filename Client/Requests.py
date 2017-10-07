from CryptoChat import RSA_encrypt
from Crypto.Cipher import AES
from Crypto import Random
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

def encrypt(plaintext, key=None, mode='RSA', target='SRV'):
    ciphertext = ''
    if mode == 'RSA':
        if target == 'SRV':
            ciphertext = RSA_encrypt(key, plaintext)
    return ciphertext

def send(sock, message, key=None):
    #generate random AES key 
    r_key = Random.new().read(AES.block_size)

    #encrypt key using server public RSA key
    

    #send key to server
    #encrypt message using AES key
    #send message to server
    length = len('%' + message)
    total_length = len(str(length)) + len('%' + message)
    message = str(total_length) + '%' + message
    sock.sendall(message.encode())


def register(sock,server_key=None,client_key=None,mode=None): 
    name = input("Username: ")
    passwd = input("Password: ")
    client_pub = b64encode(client_key.publickey().exportKey('PEM')).decode()
    print("attempting to register '{}'".format(name))
    message = 'reg#' + name + '|' + passwd #+ client_pub
    print("encrypting '{}'".format(message))
    c_request = encrypt(message,server_key)
    print("ciphertext='{}'".format(c_request))
    print("sending")
    send(sock, c_request)
    print("waiting response")
    response = recv(sock)
    print("response received: {}".format(response))


def recv_message():
    pass

def send_message():
    pass
