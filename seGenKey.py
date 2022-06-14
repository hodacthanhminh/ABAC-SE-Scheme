# libs
# pse
from se.genkey import GenKey, read_key
from se.contants import d, L

if __name__ == "__main__":
    key = GenKey(d, L)
    key_id = input('Create new key id:')
    key.write_key(key_id)
