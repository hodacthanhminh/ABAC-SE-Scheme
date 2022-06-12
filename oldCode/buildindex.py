from knn import *
from CONSTANT import *
from utils import *
import numpy as np
from mpmath import *
from genkey import *
import pandas as pd
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
        mp.dps = 30
        mp.pretty = False

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
    random_df = pd.read_json("./upload_email.json", orient='records')
    buildindex = BuildIndex(genkey.readFile())
    random_df['encrypt_index'] = list(map(buildindex.main, random_df['keyword']))
    total_export_df = pd.concat([random_df["id"], random_df["encrypt_index"]],
                                keys=['file', 'encrypt_index'], axis=1)
    count = 0
    while len(total_export_df) > 0:
        export_df = total_export_df[:10]
        total_export_df = total_export_df[10:]
        count += 1
        data = {'id': 'search{}'.format(count), 'Data': export_df.to_json(orient='records')}
        with open('./search/search-{}.json'.format(count), 'w', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False))
