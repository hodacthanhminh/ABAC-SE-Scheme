import numpy as np
from knn import *
from CONSTANT import *
from utils import *
from mpmath import *

mp.dps = 30
mp.pretty = False


def algorithm2(word, kF, Primes, Dummies):
    q = np.ones(d, dtype=float)
    word_padding = padding(word.lower(), Dummies)
    for x in range(len(word_padding)):
        if (word_padding[x] != "*"):
            pos_x = hashF(word_padding[x], kF)
            q[pos_x] = q[pos_x] * Primes[x]
        else:
            for y in string.ascii_lowercase:
                pos_xy = hashF(y, kF)
                q[pos_xy] = q[pos_xy]*Primes[x]
    q = updateRandomVector(q, Primes)
    return q


def algorithm3(s, q, Primes):
    random_vec = np.random.randint(0, s, d)
    q_extend = [[mpf(0) for _ in range(d)] for _ in range(s)]
    numbers = [np.random.random_sample() for _ in range(s-1)]
    random_bit = np.random.randint(0, 2, d)
    normalised = [round(r / sum(numbers), 10) for r in numbers]
    for j, val in enumerate(random_vec):
        q_extend[val][j] = q[j]
        prime_sum = (getRandomPrimes(Primes))*random_bit[j]
        increase = 0
        for t in range(s):
            if (t != val):
                q_extend[t][j] = prime_sum*normalised[increase]*q[j]
                increase += 1
    return q_extend


def trapdoor0(Qj, SK):
    (sk, dummies, primes, kf) = SK
    TQj_a = []
    TQj_b = []
    for value in Qj:
        qj = algorithm2(value, kf, primes, dummies)
        (qj_ea, qj_eb) = knn.EncQ(qj, sk)
        TQj_a.append(qj_ea)
        TQj_b.append(qj_eb)
    return (TQj_a, TQj_b)


def trapdoorS(Qj, SK):
    (sk, dummies, primes, kf) = SK
    TQj_a = []
    TQj_b = []
    for query in Qj:
        qj = algorithm2(query, kf, primes, dummies)
        qj_s = algorithm3(s, qj, primes)
        qj_ea = []
        qj_eb = []
        for values in qj_s:
            (qj_sea, qj_seb) = knn.EncQ(values, sk)
            qj_ea.append(qj_sea)
            qj_eb.append(qj_seb)
        TQj_a.append(qj_ea)
        TQj_b.append(qj_eb)
    return (TQj_a, TQj_b)
