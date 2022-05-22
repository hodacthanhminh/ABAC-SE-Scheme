# libs
import numpy as np
# constant
from CONSTANT import *
# function
from decimal import *
import knn
from genkey import *
from buildindex import *
from trapdoor import *
from search import *
from charm.core.math.integer import randomPrime

SK = genkey(k)


(sk, kF, Dummies, Primes) = SK
(M1, M2, S) = sk

Qj = ["thanhminh", "arteriosclerosis"]

a1 = [1 for _ in range(0, 256)]
a1_MT = knn.EncI(a1, sk)
a2 = [1 for _ in range(0, 256)]
a2_MT = knn.EncI(a2, sk)
a = []
aMT = []
aMT_a = []
aMT_b = []
aMT_a.append(a1_MT[0])
aMT_a.append(a2_MT[0])
aMT_b.append(a1_MT[1])
aMT_b.append(a2_MT[1])
a.append(a1)
a.append(a2)
aMT = (aMT_a, aMT_b)
b = []
b1 = [1 for _ in range(0, 256)]
b2 = [1 for _ in range(0, 256)]
b1_alg3 = algorithm3(3, b1)
b2_alg3 = algorithm3(3, b2)
b.append(b1_alg3)
b.append(b2_alg3)
bM1 = []
bM1_a = []
bM1_b = []
b1_alg3_e_u = []
b1_alg3_e_v = []
sum_b = np.zeros(d)
sum_back = np.zeros(d)
for x in b1_alg3:
    sum_back = np.add(x, sum_back)
    (u, v) = knn.EncQ(x, sk)
    b1_alg3_e_u.append(u)
    b1_alg3_e_v.append(v)
bM1_a.append(b1_alg3_e_u)
bM1_b.append(b1_alg3_e_v)
b2_alg3_e_u = []
b2_alg3_e_v = []
for x in b2_alg3:
    (u, v) = knn.EncQ(x, sk)
    b2_alg3_e_u.append(u)
    b2_alg3_e_v.append(v)
bM1_a.append(b2_alg3_e_u)
bM1_b.append(b2_alg3_e_v)
bM1 = (bM1_a, bM1_b)


TQj = trapdoor0(Qj, SK)
TQjs = trapdoorS(Qj, SK)

print(">> shape TQjs", np.shape(TQjs))

inner = np.inner(a, b)
inner_e = knn.Search(aMT, bM1)
print(np.shape(aMT), np.shape(bM1), np.shape(inner_e))
print(">> inner", handleSearchSSum(inner))
print(">> inner_e", handleSearchSSum(inner_e))


print(searchS(TQjs, SK, "AND"))
