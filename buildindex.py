import numpy as np
from knn import *
from CONSTANT import * 
from utils import *
from mpmath import *

mp.dps = 100
mp.pretty = False

def algorithm1(word, kF, Primes, Dummies):
    p = [mpf('1') for _ in range(0, d)]
    word_padding = padding(word,Dummies)
    for x in range (0,L):
        pos_x = hashF(word_padding[x],kF)
        p[pos_x] = p[pos_x] * (mpf(1)/Primes[x])
    p = updateRandomVector(p, Primes)
    return p


def build_index(Wi,SK):
    (sk, dummies, primes, kf) = SK
    Ii_a=[]
    Ii_b=[]
    Ii = []
    for i,value in enumerate(Wi):
        pi = algorithm1(value, kf, primes, dummies)
        Ii.append(pi)
        pi_e = knn.EncI(pi,sk)
        Ii_a.append(pi_e[0])
        Ii_b.append(pi_e[1])
    return ((Ii_a, Ii_b), Ii)

