# libs
import numpy as np
import json
# class/funcs
from .genkey import read_key, GenKey
from .search import Search
from .trapdoor import TrapDoor


class PSE:
    def __init__(self, secParams: int, lengWord: int):
        self.d = secParams
        self.L = lengWord
        self.Result = []
        self.SK = read_key()

    def set_index(self, index):
        self.Index = index['encrypt_index']
        self.File = index['id']

    def createKey(self):
        initkey = GenKey(self.d, self.L)
        initkey.write_key()

    def get_trapdoor(self):
        trapdoor = TrapDoor(self.SK, self.basic)
        return trapdoor.create_trapdoor(self.Query)

    def set_scheme(self):
        basic = input("Build Trapdoor '{'Basic: 1 , Advance: 2}]:")
        if int(basic) == 1:
            self.basic = True
        else:
            self.basic = False

    def set_query(self):
        query = input("Build Trapdoor '{'AND: 1 , OR: 2}]:")
        if int(query) == 1:
            self.andQ = True
        else:
            self.andQ = False

    def insert_query(self):
        self.set_scheme()
        print(">> Build Trapdoor as basic:", self.basic)
        val = input("Search Keyword:")
        self.Query = val.split(" ")
        self.set_query()
        self.TQj = self.get_trapdoor()
        self.Search = Search(self.andQ, self.basic)

    def set_search(self):
        for i, Ii in enumerate(self.Index):
            Im = np.asarray(json.loads(Ii))
            try:
                if (self.Search.search_result(Im, self.TQj)):
                    self.Result.append(self.File[i])

            except:
                print("{} >> broken".format(i))
                continue

    def get_result(self):
        return self.Result
