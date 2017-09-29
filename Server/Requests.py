#!/usr/bin/python3

def register(name, pwd, publickey):
    #TODO generate salt, hash salt + name, hash salt + pwd, store in db 
    pass

def receive(target, content):
    #TODO store in message db
    pass

def deliver(recipient):
    #TODO search message db for undelivered messages for recipient
    #       if they exist, send to recipient
    pass
