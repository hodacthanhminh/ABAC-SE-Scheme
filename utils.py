from CONSTANT import *
import numpy as np
import hashlib
import secrets
import string
from charm.core.math.integer import randomPrime

# generate square invertible Matrix N-demension
# Input: N
# Output Invertible square N-demension Matrix
def genInvertedMatrix(N):
    while True:
        Matrix = np.random.rand(N,N)
        if np.linalg.matrix_rank(Matrix) == N:
             return Matrix

# generate binary array S 
# Input: N
# Output Binary Array S: {0,1}^N
def createBinaryS(N):
    while True:
        S = np.random.randint(2,size=N)
        count = 0
        for i in range(0,N):
            if S[i] == 1: 
                count +=1
        if (abs(int(N/2) - count) < 2):
            return S

# hashFunction
# Input: kF - kbits in hex, character
# Output: number in [0,255]  
def hashF(kF, character):
    concat_string = "{char}{key}".format(char=character,key=kF)
    encoded_string = concat_string.encode()
    hash_code = int(hashlib.shake_256(encoded_string).hexdigest(1),16) % d
    return hash_code

def createHashKey(Dummies):
    key = ""
    while (key == ""):
        list = np.zeros((d,))
        temp_Key = secrets.token_bytes(int(k/8))
        for i,value in enumerate(A):
            pos = hashF(value,temp_Key)
            list[pos] = 1
        for j,value in enumerate(Dummies):
            pos = hashF(value,temp_Key)
            list[pos] = 1
        count=0
        for t,value in enumerate(list):
            if (value == 1): 
                count+=1
        if (count == (L + 26)):
            key = temp_Key
    return key

# generate N ramdom Dummies character
# Input: N
# Output: Array N elements contain Dummy character 
def createDummies(N): 
    list = []
    temp_list = ["*"]
    while len(list) < N:
        randomCharacter = secrets.choice(string.ascii_uppercase + string.punctuation)
        if randomCharacter not in set(temp_list):
            list.append(randomCharacter)
            temp_list.append(randomCharacter)
    return list

# generate N random Primes number
# Input: N
# Output: Array N elements contain Prime number


def createPrimes(N):
    primes = []
    while len(primes) != N:
        rand_bit = np.random.randint(3, 10)
        rand_primes = int(randomPrime(rand_bit))
        if rand_primes not in set(primes):
            primes.append(rand_primes)
    # primes.sort()
    return primes


# padding string len x to len L (x<=L)
# Input: s - string, array - padding character
# Output: <s[1|,...,s[x] | array[1],...array[L-x]>
def padding(s, array):
    if (len(s) == L): return s
    string = ''.join(str(v) for v in array)
    return s + string

# update Vector p to made p seem random
# Input: p - vector,
# Ouput: new vector 
def updateRandomVector(p):
    update_num = np.random.randint(0,abs(d-L))
    update_pos = np.random.randint(0, d, update_num)
    rand_prime = int(randomPrime(9))
    for value in update_pos:
        if isinstance(p[value], int) and p[value] == 1:
            p[value] = rand_prime
    return p 


def handleSearchSSum(result):
    sum_matrix = []
    for r_k in result:
        sum_row = []
        for r_kl in r_k:
            sum = 0
            for num in r_kl:
                sum += num
            sum_row.append(sum)
        sum_matrix.append(sum_row)
    return sum_matrix
