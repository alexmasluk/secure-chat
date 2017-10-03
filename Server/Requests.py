#!/usr/bin/python3
def send(conn, message):
    length = len('#' + message)
    total_length = len(str(length)) + len('#' + message)
    message = str(total_length) + '#' + message
    conn.sendall(message.encode())

def recv(conn):
    firstchunk = conn.recv(16).decode()
    if firstchunk:
        print(firstchunk)
        received = len(firstchunk)
        content = ''
        length, chunk = firstchunk.split('#')
        content += chunk
        while received < int(length):
            nextchunk = conn.recv(16).decode()
            received += len(nextchunk)
            content += nextchunk
        return content
    return None

def register(conn, content):
    #TODO generate salt, hash salt + name, hash salt + pwd, store in db 
    print("register!")
    username, password = content.split('|')
    print("Received user: {} pass: {}".format(username, password))
    message = "sup {} we registered you!".format(username)
    send(conn, message)
    print("sent response")
    

def send_message(conn, content):
    #TODO store in message db
    pass

def deliver(conn, content):
    #TODO search message db for undelivered messages for recipient
    #       if they exist, send to recipient
    pass
