# libs
# constant
from CONSTANT import *
# function
from genkey import *
from buildindex import *
from trapdoor import *
from search import *


class mainScheme:
    def __init__(self, secParams, lengWord):
        self.d = secParams
        self.L = lengWord
        self.Index = [
            ["thanhminh", "thplhmiwh", "temp"],
            ["math", "html", "thvnhmtng"],
            ["thanhminh", "arteriosclerosis", "thanvannh"]]
        self.Query = ["thanhminh", "arteriosclerosis"]

    def createKey(self):
        initkey = genkey(self.d, self.L)
        initkey.writeFile()

    def readKey(self):
        self.SK = genkey.readFile()

    def buildIndex(self, W):
        return build_index(W, self.SK)

    def trapDoor(self, Q, type="basic"):
        if type == "basic":
            return trapdoor0(Q, self.SK)
        else:
            return trapdoorS(Q, self.SK)

    def run(self):
        print("-----------------Get Key-----------------")
        # self.createKey()
        self.readKey()
        print("[DONE]")
        print("---------------Build Index---------------")
        index = self.buildIndex(self.Index[2])
        print("[DONE]")
        print("----------Build Trapdoor basic-----------")
        trapdoorBas = self.trapDoor(self.Query)
        print("[DONE]")
        print("-----------------Search------------------")
        print("[SEARCH MATCH]: ", search(index, trapdoorBas, "AND"))

        print("---------Build Trapdoor advanced---------")
        trapdoorAdv = self.trapDoor(self.Query, "advanced")
        print("-----------------Search------------------")
        print("[SEARCH MATCH]: ", searchS(index, trapdoorAdv, "AND"))


if __name__ == "__main__":
    scheme = mainScheme(d, L)
    scheme.run()
