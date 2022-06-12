# libs
import pandas as pd
import csv
# constant
from CONSTANT import *
# function
from genkey import *
from buildindex import *
from trapdoor import *
from search import *
import json


class mainScheme:
    def __init__(self, secParams, lengWord):
        self.d = secParams
        self.L = lengWord
        self.Result = []
        self.SK = genkey.readFile()

    def set_index(self, index):
        self.Index = index['encrypt_index']
        self.File = index['file']

    def createKey(self):
        initkey = genkey(self.d, self.L)
        initkey.writeFile()

    def trapDoor(self):
        if self.basic:
            return trapdoor0(self.Query, self.SK)
        else:
            return trapdoorS(self.Query, self.SK)

    def insert_query(self):
        basic = input("Build Trapdoor '{'Basic: 1 , Advance: 2}]:")
        if int(basic) == 1:
            self.basic = True
        else:
            self.basic = False
        print(">> Build Trapdoor as basic:", self.basic)
        val = input("Search Keyword:")
        self.Query = val.split(" ")
        self.TQj = self.trapDoor()
        print(np.shape(self.TQj))

    def set_search(self):
        for i, Ii in enumerate(self.Index):
            Im = np.asarray(json.loads(Ii))
            try:
                if self.basic:
                    if (search(Im, self.TQj, "AND")):
                        self.Result.append(self.File[i])
                else:
                    if (searchS(Im, self.TQj, "AND")):
                        self.Result.append(self.File[i])

            except:
                print("{} >> broken".format(i))
                continue

    def get_result(self):
        return self.Result


if __name__ == "__main__":
    file = input("Read Index File:")
    index = pd.read_json(file)
    scheme = mainScheme(d, L)
    scheme.set_index(index)
    scheme.run()
