# libs
import numpy as np
from mpmath import *
# class/func
from .utils import gen_inverted_matrix, create_binary_S
from .contants import d


class KNN:
    def __init__(self):
        mp.dps = 30
        mp.pretty = False

    def Key(secParams):
        M1 = gen_inverted_matrix(secParams)
        M2 = gen_inverted_matrix(secParams)
        S = create_binary_S(d)
        return (M1, M2, S)

    def EncI(p, sk):
        (M1, M2, S) = sk
        p_a = []
        p_b = []
        for i, value in enumerate(S):
            val_a = val_b = 0
            if value == 0:
                val_a = p[i]
                val_b = p[i]
                p_a.append(val_a)
                p_b.append(val_b)
            else:
                r = round(np.random.randint(0, 10)/10, 1)*p[i]
                val_a = p[i] - r
                val_b = r
                p_a.append(val_a)
                p_b.append(val_b)
        p_encrypt_a = np.matmul(p_a, np.transpose(M1))
        p_encrypt_b = np.matmul(p_b, np.transpose(M2))
        return (p_encrypt_a, p_encrypt_b)

    def EncQ(q, sk):
        (M1, M2, S) = sk
        q_a = []
        q_b = []
        invert_M1 = np.linalg.inv(M1)
        invert_M2 = np.linalg.inv(M2)
        for i, value in enumerate(S):
            val_a = val_b = 0
            if value == 1:
                val_a = val_b = q[i]
                q_a.append(val_a)
                q_b.append(val_b)
            else:
                r = round(np.random.randint(0, 10)/10, 1)*q[i]
                val_a = q[i] - r
                val_b = r
                q_a.append(val_a)
                q_b.append(val_b)
        q_encrypt_a = np.matmul(q_a, invert_M1)
        q_encrypt_b = np.matmul(q_b, invert_M2)
        return (q_encrypt_a, q_encrypt_b)

    def Search(I, Q):
        return np.inner(I[0], Q[0]) + np.inner(I[1], Q[1])
