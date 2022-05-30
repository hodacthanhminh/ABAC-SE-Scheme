from knn import *
from CONSTANT import *
from utils import *
from mpmath import *

mp.dps = 100
mp.pretty = False


def algorithm1(word, kF, Primes, Dummies):
    p = [mpf('1') for _ in range(0, d)]
    word_padding = padding(word.lower(), Dummies)
    for x in range(len(word_padding)):
        pos_x = hashF(word_padding[x], kF)
        p[pos_x] = p[pos_x] * (mpf(1)/Primes[x])
    p = updateRandomVector(p, Primes)
    return p


def build_index(Wi, SK):
    (sk, dummies, primes, kf) = SK
    Ii_a = []
    Ii_b = []
    for value in Wi:
        pi = algorithm1(value, kf, primes, dummies)
        (pi_ea, pi_eb) = knn.EncI(pi, sk)
        Ii_a.append(pi_ea)
        Ii_b.append(pi_eb)
    return (Ii_a, Ii_b)
