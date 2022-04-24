from genkey import *
from hash import *


secret_key = genkey(128)

print(hashF(secret_key[1],"T"))
print(hashF(secret_key[1],"M"))