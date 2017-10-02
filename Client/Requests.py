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

def register(sock):
    name = input("Username: ")
    passwd = input("Password: ")
    print("attempting to register '{}'".format(name))
    request = 'reg%' + name + '|' + passwd
    print("sending")
    send(sock, request)
    print("waiting response")
    response = recv(sock)
    print("response received: {}".format(response))


def receive():
    pass
