# libs
import numpy as np
import json
# class/funcs
from .genkey import read_key, GenKey, read_key_file
from .search import Search
from .trapdoor import TrapDoor


class PSE:
    def __init__(self, secParams: int, lengWord: int):
        self.d = secParams
        self.L = lengWord
        self.Result = []

    def set_key(self, key_path):
        self.SK = read_key(key_path)

    def set_key_file(self, key):
        self.SK = read_key_file(key)

    def set_index(self, index):
        self.Index = index['encrypt_index']
        self.File = index['id']

    def set_trapdoor(self, data):
        self.TQj = data

    def get_trapdoor(self):
        return self.TQj

    def create_key(self, key_path, key_id):
        initkey = GenKey(self.d, self.L)
        initkey.write_key(key_path, key_id)

    def create_trapdoor(self):
        trapdoor = TrapDoor(self.SK, self.basic)
        self.TQj = trapdoor.create_trapdoor(self.Query)
        return self.TQj

    def set_detail(self, basic=True, query=True):
        if basic:
            self.basic = True
        else:
            self.basic = False
        if query:
            self.andQ = True
        else:
            self.andQ = False
        self.Search = Search(self.andQ, self.basic)

    def insert_query(self, query):
        self.Query = query
        self.create_trapdoor()
        self.Result = []

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
