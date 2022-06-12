# libs
# pse
from se.genkey import GenKey, read_key
from se.contants import d, L

if __name__ == "__main__":
    key = GenKey(d, L)
    key.write_key()
    (sk, dummies, primes, kf) = read_key()
