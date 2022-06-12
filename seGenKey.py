# libs
# pse
from se.genkey import GenKey
from se.contants import d, L

if __name__ == "__main__":
    key = GenKey(d, L)
    key.write_file()
