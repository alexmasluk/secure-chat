from Crypto.PublicKey import RSA
from base64 import b64decode, b64encode

def RSA_encrypt(key, ptxt):
    cbytes = key.encrypt(message.encode(), 0)[0]
    return b64encode(cbytes)

