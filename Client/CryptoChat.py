from Crypto.PublicKey import RSA
from base64 import b64decode, b64encode

def RSA_encrypt(key, ptxt):
    print('plaintext == "{}"'.format(ptxt))
    cbytes = key.encrypt(ptxt.encode(), 0)[0]
    return b64encode(cbytes).decode()

