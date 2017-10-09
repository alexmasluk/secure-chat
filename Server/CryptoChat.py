from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random
from base64 import b64decode, b64encode

def pad(s):
    b = AES.block_size
    return s + (b - len(s) % b) * chr(b - len(s) % b)

def unpad(s):
    return s[:-ord(s[len(s)-1:])]

def AES_encrypt(key, ptxt):
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    ptxt = pad(ptxt)
    cbytes = iv + cipher.encrypt(ptxt.encode())
    return b64encode(cbytes).decode()

def AES_decrypt(key, ctxt):
    cbytes = b64decode(ctxt)
    iv = cbytes[:AES.block_size]
    msg = cbytes[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CFB, iv)
    pbytes = cipher.decrypt(msg)
    ptxt = unpad(pbytes)
    return ptxt.decode()

def RSA_encrypt(key, ptxt):
    cbytes = key.encrypt(ptxt.encode(), 0)[0]
    return b64encode(cbytes).decode()

def RSA_decrypt(key, ctxt):
    ctxt_decoded = b64decode(ctxt)
    pbytes = key.decrypt(ctxt_decoded)
    return pbytes.decode()

