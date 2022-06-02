from knn import *
from CONSTANT import *
from utils import *
from mpmath import *
from genkey import *
import pandas as pd
import csv
from funmark import Benchmark


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
            print("Doc {} - Key {}".format(self.Doc, self.KeyWord))
            pi = self.algorithm1(value)
            (pi_ea, pi_eb) = knn.EncI(pi, self.sk)
            Ii_a.append(pi_ea)
            Ii_b.append(pi_eb)
        return (Ii_a, Ii_b)


if __name__ == "__main__":
    emails_df = pd.read_csv("./parsing_emails.csv",
                            converters={"keyword": lambda x: x.strip("[]").replace("'", "").split(", ")})
    buildindex = BuildIndex(genkey.readFile())
    random_df = emails_df.sample(n=5000)
    random_df['encrypt_index'] = list(map(buildindex.main, random_df['keyword']))

    export_df = pd.concat([random_df['file'], random_df["encrypt_index"]], axis=1, keys=['file', 'encrypt_index'])
    export_df.to_pickle('./encryptIndex_20.csv')
