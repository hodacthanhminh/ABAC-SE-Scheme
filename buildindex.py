import numpy as np
import knn
from CONSTANT import * 
from utils import *

def algorithm1(word, kF, Primes, Dummies):
    p = [int(1) for _ in range(0, d)]
    word_padding = padding(word,Dummies)
    for x in range (0,L):
        pos_x = hashF(word_padding[x],kF)
        p[pos_x] = p[pos_x] * float(1/Primes[x])
    p = updateRandomVector(p)
    return p


def build_index(Wi,SK):
    (sk,kF,Dummies,Primes) = SK
    Ii_a=[]
    Ii_b=[]
    for i,value in enumerate(Wi):
        pi = algorithm1(value,kF,Primes,Dummies)
        pi_e = knn.EncI(pi,sk)
        Ii_a.append(pi_e[0])
        Ii_b.append(pi_e[1])
    return (Ii_a, Ii_b)

