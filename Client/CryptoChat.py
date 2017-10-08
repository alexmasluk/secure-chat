from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random
from base64 import b64decode, b64encode


def pad(s):
    b = AES.block_size
    return s + (b - len(s) % b) * chr(b - len(s) % b)

def unpad(s):
    return s[:-ord(s[len(s)-1:])]

def RSA_encrypt(key, ptxt):
    cbytes = key.encrypt(ptxt.encode(), 0)[0]
    return b64encode(cbytes).decode()

def AES_encrypt(key, ptxt):
    #print('aes key == {}'.format(key))
    iv = Random.new().read(AES.block_size)
    #print('i   v   == {}'.format(iv))
    cipher = AES.new(key, AES.MODE_CFB, iv)
    ptxt = pad(ptxt)
    #print('pbytes  == {}'.format(ptxt.encode()))
    cbytes = iv + cipher.encrypt(ptxt.encode())
    #print('cbytes  == {}'.format(cbytes))
    return b64encode(cbytes).decode()
