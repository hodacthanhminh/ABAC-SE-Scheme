from knn import *
from CONSTANT import *
from utils import *
from mpmath import *
from genkey import *
import pandas as pd
import numpy as np
import json
from json import JSONEncoder


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


class BuildIndex:
    def __init__(self, SK):
        (sk, dummies, primes, kf) = SK
        self.sk = sk
        self.dummies = dummies
        self.primes = primes
        self.kf = kf
        self.KeyWord = 0
        self.Doc = 0

    def algorithm1(self, word):
        p = np.ones(d, dtype=float)
        word_padding = padding(word, self.dummies)
        for x in range(0, len(word_padding)):
            pos_x = hashF(word_padding[x], self.kf)
            p[pos_x] = p[pos_x] / self.primes[x]
        p = updateRandomVector(p, self.primes)
        return p

    def main(self, Wi):
        Ii_a = []
        Ii_b = []
        self.Doc += 1
        for value in Wi:
            self.KeyWord += 1
            print("Doc {} - Key No.{} - Word {}".format(self.Doc, self.KeyWord, value))
            pi = self.algorithm1(value)
            (pi_ea, pi_eb) = knn.EncI(pi, self.sk)
            Ii_a.append(pi_ea)
            Ii_b.append(pi_eb)
        return json.dumps(np.array([Ii_a, Ii_b], dtype=np.ndarray), cls=NumpyArrayEncoder)


if __name__ == "__main__":
    emails_df = pd.read_json("./export_json.json")
    buildindex = BuildIndex(genkey.readFile())
    number_of_file = int(input("Enter number of file:"))
    random_df = emails_df.sample(n=number_of_file)
    import timeit
    start_timer = timeit.default_timer()
    random_df['encrypt_index'] = list(map(buildindex.main, random_df['keyword']))
    print("finish after {} second".format(round(timeit.default_timer() - start_timer, 2)))
    total_export_df = pd.concat([random_df["ID"], random_df["encrypt_index"]],
                                keys=['file', 'encrypt_index'], axis=1)
    count = 0
    while len(total_export_df) > 0:
        export_df = total_export_df[:2000]
        total_export_df = total_export_df[2000:]
        count += 1
        data = {'ID': 'search{}'.format(count), 'Data': export_df.to_json(orient='records')}
        with open('search-{}.json'.format(count), 'w', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False))
