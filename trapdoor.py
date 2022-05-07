import numpy as np
import knn
from CONSTANT import * 
from utils import *

def algorithm2(word, kF, Primes, Dummies):
    q = np.ones((d,), dtype=np.float64)
    word_padding = padding(word,Dummies)
    for x in range (0,L):
        if (word_padding[x] != "*"): 
            pos_x = hashF(word_padding[x],kF)
            q[pos_x] = q[pos_x]*np.float64(Primes[x])
        else:
            for y in range (0,26 + L):
                if ( 0 <= y < 26):
                    pos_xy = hashF(A[y],kF)
                else:
                    pos_xy = hashF(Dummies[y-26],kF)
                q[pos_xy] = q[pos_xy]*np.float64(Primes[x])
    q = updateRandomVector(q,Primes)
    return q


def trapdoor(Qj,SK):
    (sk,kF,Dummies,Primes) = SK
    TQj_a=[]
    TQj_b=[]
    for j,value in enumerate(Qj):
        qj = algorithm2(value,kF,Primes,Dummies)
        (qj_ea, qj_eb) = knn.EncQ(qj,sk)
        TQj_a.append(qj_ea)
        TQj_b.append(qj_eb)
    return (TQj_a, TQj_b)