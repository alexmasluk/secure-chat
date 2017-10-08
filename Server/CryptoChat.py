from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random
from base64 import b64decode, b64encode

def pad(s):
    b = AES.block_size
    return s + (b - len(s) % b) * chr(b - len(s) % b)

def unpad(s):
    return s[:-ord(s[len(s)-1:])]

def AES_decrypt(key, ctxt):
    cbytes = b64decode(ctxt)
    #key = b64decode(key)
    #print("key = {}".format(key))
    iv = cbytes[:AES.block_size]
    #print("i v = {}".format(iv))
    msg = cbytes[AES.block_size:]
    #print("msg = {}".format(msg))
    cipher = AES.new(key, AES.MODE_CFB, iv)
    print("msglen = {}".format(len(msg)))

    pbytes = cipher.decrypt(msg)
    #print("pbytes len={}".format(len(pbytes)))
    #print("pbytes    ={}".format(pbytes))
    ptxt = unpad(pbytes)
    #print("ptxt = {}".format(ptxt))
    return ptxt.decode()

def RSA_encrypt(key, ptxt):
    cbytes = key.encrypt(ptxt.encode(), 0)[0]
    return b64encode(cbytes).decode()

def RSA_decrypt(key, ctxt):
    ctxt_decoded = b64decode(ctxt)
    pbytes = key.decrypt(ctxt_decoded)
    print(str(pbytes, errors='ignore'))
    return pbytes.decode()

