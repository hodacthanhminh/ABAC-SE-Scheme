# libs
import numpy as np
# constant
from CONSTANT import *
# function
import knn
from genkey import *
from buildindex import *
from trapdoor import *
from search import *

SK = genkey(k)


(sk,kF,Dummies,Primes) = SK  
print(Primes)
(M1,M2,S) = sk

Qj =["thanhminh","t***"]

TQj= trapdoor(Qj,SK)

print(search(TQj,SK,"AND"))











