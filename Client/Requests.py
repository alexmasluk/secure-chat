from CryptoChat import RSA_encrypt

def recv(sock):
    firstchunk = sock.recv(16).decode()
    received = len(firstchunk)
    content = ''
    length, chunk = firstchunk.split('#')
    content += chunk
    while received < int(length):
        nextchunk = sock.recv(16).decode()
        received += len(nextchunk)
        content += nextchunk
    return content

def send(sock, message):
    length = len('#' + message)
    total_length = len(str(length)) + len('#' + message)
    message = str(total_length) + '#' + message
    sock.sendall(message.encode())

def encrypt(plaintext, key=None, mode='RSA', target='SRV'):
    ciphertext = ''
    if mode == 'RSA':
        if target == 'SRV':
            ciphertext = RSA_encrypt(key, plaintext)
    return ciphertext

def register(sock,key=None,mode=None): 
    name = input("Username: ")
    passwd = input("Password: ")
    print("attempting to register '{}'".format(name))
    request = 'reg%' + name + '|' + passwd
    print("encrypting")
    c_request = encrypt(request,key)
    print("sending")
    send(sock, request)
    print("waiting response")
    response = recv(sock)
    print("response received: {}".format(response))


def receive():
    pass
