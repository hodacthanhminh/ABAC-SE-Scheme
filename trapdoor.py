import numpy as np
import knn
from CONSTANT import *
from utils import *


def algorithm2(word, kF, Primes, Dummies):
    q = [int(1) for _ in range(0, d)]
    word_padding = padding(word, Dummies)
    for x in range(0, L):
        if (word_padding[x] != "*"):
            pos_x = hashF(word_padding[x], kF)
            q[pos_x] = q[pos_x]*Primes[x]
        else:
            for y in range(0, 26):
                pos_xy = hashF(A[y], kF)
                q[pos_xy] = q[pos_xy]*Primes[x]
            for t in range(0, L):
                pos_xy = hashF(Dummies[t], kF)
                q[pos_xy] = q[pos_xy]*Primes[x]
    q = updateRandomVector(q, Primes)
    return q


def algorithm3(s, q, Primes):
    random_vec = np.random.randint(0, s, d)
    q_extend = [[int(0) for _ in range(0, d)] for _ in range(0, s)]
    random_bit = np.random.randint(0, 2)
    prime_sum = (getRandomPrimes(Primes)-1)*random_bit
    for j, val in enumerate(random_vec):
        q_extend[val][j] = q[j]
        numbers = [np.random.random_sample() for _ in range(s-1)]
        normalised = [r / sum(numbers) for r in numbers]
        increase = 0
        for t in range(0, s):
            if (t != val):
                q_extend[t][j] = prime_sum*normalised[increase]*q[j]
                increase += 1
    return q_extend


def trapdoor0(Qj, SK):
    (sk, kF, Dummies, Primes) = SK
    TQj_a = []
    TQj_b = []
    for j, value in enumerate(Qj):
        qj = algorithm2(value, kF, Primes, Dummies)
        (qj_ea, qj_eb) = knn.EncQ(qj, sk)
        TQj_a.append(qj_ea)
        TQj_b.append(qj_eb)
    return (TQj_a, TQj_b)


def trapdoorS(Qj, SK):
    (sk, kF, Dummies, Primes) = SK
    TQj_a = []
    TQj_b = []
    for value in Qj:
        qj = algorithm2(value, kF, Primes, Dummies)
        qj_s = algorithm3(s, qj, Primes)
        qj_ea = []
        qj_eb = []
        for value in qj_s:
            (qj_sea, qj_seb) = knn.EncQ(value, sk)
            qj_ea.append(qj_sea)
            qj_eb.append(qj_seb)
        TQj_a.append(qj_ea)
        TQj_b.append(qj_eb)
    return (TQj_a, TQj_b)
