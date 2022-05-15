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
    q = updateRandomVector(q)
    return q

def algorithm3(s,q):
    print(s)
    random_vec = np.random.randint(0,s,d)
    q_extend = np.zeros([s,d])
    for j,val in enumerate(random_vec):
        q_extend[val][j] = q[j]
        prime_sum = (np.random.choice(outP) - 1)
        numbers = [np.random.random_sample() for _ in range(s-1)]
        normalised = [r / sum(numbers) for r in numbers] 
        increase = 0
        for t in range(0,s):
            if (t != val):
                q_extend[t][j] = prime_sum*normalised[increase]*q[j]
                increase +=1
        
    return q_extend


def trapdoor(Qj,SK):
    (sk,kF,Dummies,Primes) = SK
    TQj_a=[]
    TQj_b=[]
    for j,value in enumerate(Qj):
        qj = algorithm2(value,kF,Primes,Dummies)
        qj_s = algorithm3(s,qj)
        qj_ea = []
        qj_eb = []
        for l in range(0,s):
            (qj_sea, qj_seb) = knn.EncQ(qj_s[l],sk)
            qj_ea.append(qj_sea)
            qj_eb.append(qj_seb)
        TQj_a.append(qj_ea)
        TQj_b.append(qj_eb)
    return (TQj_a, TQj_b)