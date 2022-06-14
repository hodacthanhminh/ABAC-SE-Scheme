from copyreg import pickle
from knn import *
from CONSTANT import *
from utils import *
# from pyspark import cloudpickle
import pickle


class genkey:
    def __init__(self, secParam, lengWord):
        self.secParam = secParam
        self.lengWord = lengWord
        self.sk = knn.Key(self.secParam)
        self.dummies = createDummies(self.lengWord)
        self.primes = createPrimes(self.lengWord)
        self.kf = createHashKey(self.dummies)

    def writeFile(self):
        with open('genKey.txt', 'wb') as filehandle:
            cloudpickle.dump(obj={'sk': self.sk, 'dummies': self.dummies,
                                  'primes': self.primes, 'kf': self.kf}, file=filehandle)
            filehandle.close()

    def readFile():
        with open('genKey.txt', 'rb') as filehandle:
            data = pickle.load(filehandle)
            filehandle.close()

        sk = data['sk']
        primes = data['primes']
        dummies = data['dummies']
        kf = data['kf']
        return (sk, dummies, primes, kf)

    def main(self):
       self.writeFile()


if __name__ == "__main__":
    createKey = genkey(d, L)
    createKey.main()
