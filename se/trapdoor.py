# libs
import numpy as np
from mpmath import *
import string
# class/func
from .knn import KNN
from .contants import s, d, L
from .utils import hash_F, padding, update_random_vector, get_random_primes

mp.dps = 30
mp.pretty = False


class TrapDoor:
    def __init__(self, SK: tuple, basic: bool):
        (sk, dummies, primes, kf) = SK
        self.sk = sk
        self.dummies = dummies
        self.primes = primes
        self.kf = kf
        self.basic = basic

    def algorithm2(self, word):
        q = np.ones(d, dtype=float)
        word_padding = padding(word.lower(), self.dummies)
        for x in range(len(word_padding)):
            if (word_padding[x] != "*"):
                pos_x = hash_F(word_padding[x], self.kf)
                q[pos_x] = q[pos_x] * self.primes[x]
            else:
                for y in string.ascii_lowercase:
                    pos_xy = hash_F(y, self.kf)
                    q[pos_xy] = q[pos_xy]*self.primes[x]
        q = update_random_vector(q, self.primes)
        return q

    def algorithm3(self, q):
        random_vec = np.random.randint(0, s, d)
        q_extend = [[mpf(0) for _ in range(d)] for _ in range(s)]
        numbers = [np.random.random_sample() for _ in range(s-1)]
        random_bit = np.random.randint(0, 2, d)
        normalised = [round(r / sum(numbers), 10) for r in numbers]
        for j, val in enumerate(random_vec):
            q_extend[val][j] = q[j]
            prime_sum = (get_random_primes(self.primes))*random_bit[j]
            increase = 0
            for t in range(s):
                if (t != val):
                    q_extend[t][j] = prime_sum*normalised[increase]*q[j]
                    increase += 1
        return q_extend

    def trapdoor0(self):
        TQj_a = []
        TQj_b = []
        for value in self.Qj:
            qj = self.algorithm2(value)
            (qj_ea, qj_eb) = KNN.EncQ(qj, self.sk)
            TQj_a.append(qj_ea)
            TQj_b.append(qj_eb)
        return (TQj_a, TQj_b)

    def trapdoorS(self):
        TQj_a = []
        TQj_b = []
        for query in self.Qj:
            qj = self.algorithm2(query)
            qj_s = self.algorithm3(qj)
            qj_ea = []
            qj_eb = []
            for values in qj_s:
                (qj_sea, qj_seb) = KNN.EncQ(values, self.sk)
                qj_ea.append(qj_sea)
                qj_eb.append(qj_seb)
            TQj_a.append(qj_ea)
            TQj_b.append(qj_eb)
        return (TQj_a, TQj_b)

    def create_trapdoor(self, Qj):
        self.Qj = Qj
        if (self.basic):
            return self.trapdoor0()
        else:
            return self.trapdoorS()
