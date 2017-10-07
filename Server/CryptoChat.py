from Crypto.PublicKey import RSA
from base64 import b64decode, b64encode

def RSA_encrypt(key, ptxt):
    cbytes = key.encrypt(ptxt.encode(), 0)[0]
    return b64encode(cbytes).decode()

def RSA_decrypt(key, ctxt):
    ctxt_decoded = b64decode(ctxt)
    pbytes = key.decrypt(ctxt_decoded)
    print(str(pbytes, errors='ignore'))
    return pbytes.decode()

