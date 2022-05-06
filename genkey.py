import secrets
import knn
from CONSTANT import *
from utils import *

def genkey(k):
    sk = knn.Key(d)
    KF = secrets.token_bytes(int(k/8))
    Dummies = createDummys(L)
    Primes = createPrimes(L)  
    return (sk,KF,Dummies, Primes)
