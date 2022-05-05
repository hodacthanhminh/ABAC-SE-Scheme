from CONSTANT import *
import numpy as np
import hashlib
import secrets
import string

# generate square invertible Matrix N-demension
# Input: N
# Output Invertible square N-demension Matrix
def genInvertedMatrix(N):
    while True:
        Matrix = np.random.rand(N,N)
        if np.linalg.matrix_rank(Matrix) == N:
             return Matrix

# hashFunction
# Input: kF - kbits in hex, character
# Output: number in [0,255]  
def hashF(kF, character):
    concat_string = "{char}{key}".format(char=character,key=kF)
    encoded_string = concat_string.encode()
    hash_code = int(hashlib.shake_256(encoded_string).hexdigest(1),16) % d
    return hash_code

# generate N ramdom Dummies character
# Input: N
# Output: Array N elements contain Dummy character 
def createDummys(N): 
    list = []
    while len(list) < N:
        randomCharacter = secrets.choice(string.ascii_uppercase + string.digits + string.punctuation);
        if randomCharacter not in list:
            list.append(randomCharacter)
    return list

# generate N random Primes number
# Input: N
# Output: Array N elements contain Prime number
def createPrimes(N):
    rand_pos = np.random.randint(0,len(smallp) - L)
    return smallp[rand_pos:rand_pos+N]

# padding string len x to len L (x<=L)
# Input: s - string, array - padding character
# Output: <s[1|,...,s[x] | array[1],...array[L-x]>
def padding(s, array):
    if (len(s) == L): return s
    string = ''.join(str(v) for v in array)
    print(type(string), type(s))
    return s + string

# update Vector p to made p seem random
# Input: p - vector, Primes - array length L of primes number
# Ouput: new vector 
def updateRandomVector(p, Primes):
    update_num = np.random.randint(0,abs(d-L))
    update_pos = np.random.randint(0,d)
    prime_set = set(Primes)
    rand_yet = True
    while rand_yet:
        rand_prime = np.random.choice(smallp)
        rand_yet = rand_prime in prime_set
    while (update_num > 0) and (update_pos < d):
        if (int(p[update_pos]) == 1):
            update_num-=1
            p[update_pos]= rand_prime
        update_pos+=1
    return p 