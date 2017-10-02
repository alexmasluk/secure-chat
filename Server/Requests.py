#!/usr/bin/python3
def send(conn, message):
    length = len('#' + message)
    total_length = len(str(length)) + len('#' + message)
    message = str(total_length) + '#' + message
    conn.sendall(message.encode())

def register(conn, content):
    #TODO generate salt, hash salt + name, hash salt + pwd, store in db 
    print("register!")
    username, password = content.split('|')
    print("Received user: {} pass: {}".format(username, password))
    message = "sup {} we registered you!".format(username)
    send(conn, message)
    print("sent response")
    

def receive(conn, content):
    #TODO store in message db
    pass

def deliver(conn, content):
    #TODO search message db for undelivered messages for recipient
    #       if they exist, send to recipient
    pass
