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
    def __init__(self, secParams, lengWord, index):
        self.d = secParams
        self.L = lengWord
        self.Index = index['encrypt_index']
        self.File = index['file']
        self.Result = []

    def createKey(self):
        initkey = genkey(self.d, self.L)
        initkey.writeFile()

    def readKey(self):
        self.SK = genkey.readFile()

    def trapDoor(self, type="basic"):
        if type == "basic":
            return trapdoor0(self.Query, self.SK)
        else:
            return trapdoorS(self.Query, self.SK)

    def insertQuery(self):
        val = input("Search Keyword:")
        self.Query = val.split(" ")

    def run(self):
        print("-----------------Get Key-----------------")
        # self.createKey()
        self.readKey()
        print("[DONE]")
        print("---------------Build Index---------------")
        print("[DONE]")
        print("--------Enter Your Search Keyword--------")
        self.insertQuery()
        # print("----------Build Trapdoor basic-----------")
        # trapdoorBas = self.trapDoor()
        print("[DONE]")
        print("-----------------Search------------------")
        # for i, Ii in enumerate(self.Index):
        #     if (search(Ii[1], trapdoorBas, "AND")):
        #         self.Result.append(Ii[0])
        # print("[SEARCH MATH FILE]: ", self.Result)
        # self.Result = []
        print("---------Build Trapdoor advanced---------")
        trapdoorAdv = self.trapDoor("advanced")
        # print("-----------------Search------------------")
        for i, Ii in enumerate(self.Index):
            Im = np.asarray(json.loads(Ii))
            # print(i,np.shape(Im))
            try:
                if (searchS(Im, trapdoorAdv, "AND")):
                    self.Result.append(self.File[i])
            except:
                print("{} >> broken".format(i))
                continue

        print("[SEARCH MATH FILE]: ", self.Result)


if __name__ == "__main__":
    file = input("Read Index File:")
    index = pd.read_json(file)
    scheme = mainScheme(d, L, index)
    scheme.run()
