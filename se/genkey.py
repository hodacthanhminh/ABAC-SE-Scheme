# libs
import json
import pandas as pd
# class/funcs
from .knn import KNN
from .utils import create_dummies, create_primes, create_hash_key, NumpyArrayEncoder


class GenKey:
    def __init__(self, secParam, lengWord):
        self.secParam = secParam
        self.lengWord = lengWord
        self.sk = KNN.Key(self.secParam)
        self.dummies = create_dummies(self.lengWord)
        self.primes = create_primes(self.lengWord)
        self.kf = create_hash_key(self.dummies)

    def write_key(self):
        key_id = input('Create new key id:')
        with open('./local/key/key-{}.json'.format(key_id), 'w') as filehandle:
            sk_str = json.dumps({'sk': self.sk, 'dummies': self.dummies, 'primes': self.primes,
                                'kf': str(self.kf, 'latin1')}, cls=NumpyArrayEncoder)
            data = json.dumps([{'id': 'key-{}'.format(key_id), 'data': sk_str}])
            filehandle.write(data)


def read_key() -> tuple:
    key_id = input('Insert your key id:')
    key = pd.read_json('./local/key/key-{}.json'.format(key_id), orient='records')
    data = json.loads(key['data'][0])
    sk = tuple(data['sk'])
    primes = data['primes']
    dummies = data['dummies']
    kf = bytes(data['kf'], 'latin1')
    return (sk, dummies, primes, kf)
