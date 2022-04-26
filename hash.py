from genkey import *

import hashlib

def hashF(KF, character):
    encoded_string = character.encode()
    byte_array = bytearray(encoded_string)
    hash_code = '{0:08b}'.format(int(hashlib.blake2s(byte_array, digest_size=1, key=KF).hexdigest(),16))
    return hash_code