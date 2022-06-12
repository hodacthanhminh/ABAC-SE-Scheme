# libs
import pickle
from pyspark import cloudpickle
# class/funcs
from .knn import KNN
from .utils import create_dummies, create_primes, create_hash_key


class GenKey:
    def __init__(self, secParam, lengWord):
        self.secParam = secParam
        self.lengWord = lengWord
        self.sk = KNN.Key(self.secParam)
        self.dummies = create_dummies(self.lengWord)
        self.primes = create_primes(self.lengWord)
        self.kf = create_hash_key(self.dummies)

    def write_file(self):
        key_id = input('Enter key id')
        with open('./local/key/key-{}.json'.format(key_id), 'wb') as filehandle:
            data = [{'id': 'key-{}'.format(key_id), 'sk': self.sk, 'dummies': self.dummies,
                     'primes': self.primes, 'kf': self.kf}]
            filehandle.close()


def read_file():
    with open('genKey.txt', 'rb') as filehandle:
        data = pickle.load(filehandle)
        filehandle.close()

    sk = data['sk']
    primes = data['primes']
    dummies = data['dummies']
    kf = data['kf']
    return (sk, dummies, primes, kf)
