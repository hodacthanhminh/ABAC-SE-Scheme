# libs
import numpy as np
import hashlib
import secrets
import string
from charm.core.math.integer import randomPrime
from mpmath import *
from json import JSONEncoder
# const
from .contants import *

# generate square invertible Matrix N-demension
# Input: N
# Output Invertible square N-demension Matrix


def gen_inverted_matrix(N):
    while True:
        Matrix = np.random.rand(N, N)
        if np.linalg.matrix_rank(Matrix) == N:
            return np.array(Matrix, dtype=float)

# generate binary array S
# Input: N
# Output Binary Array S: {0,1}^N


def create_binary_S(N):
    while True:
        S = np.random.randint(2, size=N)
        count = 0
        for i in range(0, N):
            if S[i] == 1:
                count += 1
        if (abs(int(N/2) - count) < 2):
            return S

# hashFunction
# Input: kF - kbits in hex, character
# Output: number in [0,255]


def hash_F(kF, character):
    concat_string = "{char}{key}".format(char=character, key=kF)
    encoded_string = concat_string.encode()
    hash_code = int(hashlib.shake_256(encoded_string).hexdigest(1), 16) % d
    return hash_code


def create_hash_key(Dummies):
    key = ""
    while (key == ""):
        list = np.zeros((d,))
        temp_Key = secrets.token_bytes(int(k/8))
        for alphabet in string.ascii_lowercase:
            pos = hash_F(alphabet, temp_Key)
            list[pos] = 1
        for dump in Dummies:
            pos = hash_F(dump, temp_Key)
            list[pos] = 1
        count = 0
        for value in list:
            if (value == 1):
                count += 1
        if (count == (L + 26)):
            key = temp_Key
    return key

# generate N ramdom Dummies character
# Input: N
# Output: Array N elements contain Dummy character


def create_dummies(N):
    list = []
    temp_list = ["*"]
    while len(list) < N:
        randomCharacter = secrets.choice(string.ascii_uppercase + string.punctuation)
        if randomCharacter not in set(temp_list):
            list.append(randomCharacter)
            temp_list.append(randomCharacter)
    return np.array(list, dtype=object)

# generate N random Primes number
# Input: N
# Output: Array N elements contain Prime number


def create_primes(N):
    primes = []
    while len(primes) != N:
        rand_bit = np.random.randint(3, 10)
        rand_primes = int(randomPrime(rand_bit))
        if rand_primes not in set(primes):
            primes.append(rand_primes)
    return primes


# padding string len x to len L (x<=L)
# Input: s - string, array - padding character
# Output: <s[1|,...,s[x] | array[1],...array[L-x]>
def padding(s, array):
    if (len(s) == L):
        return s
    string = ''.join(str(v) for v in array)
    return s + string[:L - len(s)]

# update Vector p to made p seem random
# Input: p - vector,
# Ouput: new vector


def update_random_vector(p, Primes):
    update_num = np.random.randint(0, abs(d-L))
    update_pos = np.random.randint(0, d, update_num)
    rand_prime = get_random_primes(Primes)
    for value in update_pos:
        if p[value] == 1:
            p[value] = rand_prime
    return p


def get_random_primes(Primes):
    while True:
        bit_present = np.random.randint(3, 10)
        random_prime = int(random_prime(bit_present))
        if random_prime not in set(Primes):
            return random_prime


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)
