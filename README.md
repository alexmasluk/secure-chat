# Secure Chat

**This is the repo for our group project**

What we have so far
-Server and Client each have a sqlite3 database
-Each db has a user and message table 
-Server has a private RSA key
-Each client has a copy of server's public RSA key
-Each client has an RSA key pair 

1) Server loads RSA key
2) Server listens for client connections
3) Client looks for client RSA key pair, generating one if needed
4) Client loads server public key
5) Client connects to server
6) Server dispatches thread for each client that connects
7) Client and server can send message formatted as follows
MESSAGE_LENGTH%RSA_pub(random_AES_key)%random_AES_key(request_type#msg_content1|msg_content2|..|msg_contentN)
This works as follows:

    a) Sender generates a random AES key
    b) Sender encrypts the AES key using receiver's public RSA key
    c) Sender encrypts message content using the AES key
    d) Sender concats message length, RSA-encrypted AES key, and AES-encrypted message 

The following message content formats are supported:
Register / Login
req#username|password|RSA_public_key

Send message
snd#target_usr|msg_content

Retrieve message
rcv#username


------------------
Require the second client because we need to test if the DB will sync with each other when we implement ONE TIME KEY schema.
It is cruial for both client to have sync DB so that the derive key will be the same

-------------------------------------
# How to run

1. Setup and run the server
    Server can be run from AWS with a correct security policy
      Base: open port 22, 10000
      
2. Setup the client 
    The client will be able to login if and only if the server is running.
    


**Important all database must be sync.
- If not sure please delete data in database file for all three database in both clients and server.
- Another option is to choose one client and delete the other. Copy the chosen client and use it as a second client in testing.



