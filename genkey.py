import secrets
import knn
from CONSTANT import *
from utils import *

def genkey(k):
    sk = knn.Key(d)
    Dummies = createDummies(L)
    Primes = createPrimes(L)  
    KF = createHashKey(Dummies)
    return (sk,KF,Dummies, Primes)
