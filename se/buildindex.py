# libs
import numpy as np
from mpmath import *
import json
# class/funcs
from .knn import KNN
from .contants import d
from .utils import hash_F, update_random_vector, NumpyArrayEncoder, padding


class BuildIndex:
    def __init__(self, SK):
        (sk, dummies, primes, kf) = SK
        self.sk = sk
        self.dummies = dummies
        self.primes = primes
        self.kf = kf
        self.KeyWord = 0
        self.Doc = 0
        mp.dps = 30
        mp.pretty = False

    def algorithm1(self, word):
        p = np.ones(d, dtype=float)
        word_padding = padding(word, self.dummies)
        for x in range(0, len(word_padding)):
            pos_x = hash_F(word_padding[x], self.kf)
            p[pos_x] = p[pos_x] / self.primes[x]
        p = update_random_vector(p, self.primes)
        return p

    def main(self, Wi):
        Ii_a = []
        Ii_b = []
        self.Doc += 1
        for value in Wi:
            self.KeyWord += 1
            # print("Doc {} - Key No.{} - Word {}".format(self.Doc, self.KeyWord, value))
            pi = self.algorithm1(value)
            (pi_ea, pi_eb) = KNN.EncI(pi, self.sk)
            Ii_a.append(pi_ea)
            Ii_b.append(pi_eb)
        return json.dumps(np.array([Ii_a, Ii_b], dtype=np.ndarray), cls=NumpyArrayEncoder)
