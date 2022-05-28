# libs
# constant
from CONSTANT import *
# function
from genkey import *
from buildindex import *
from trapdoor import *
from search import *

SK = genkey(k)


(sk, kF, Dummies, Primes) = SK
(M1, M2, S) = sk

Qj = ["thanhmi**", "arteriosclerosis"]
Wi = [["thanhminh", "thplhmiwh", "temp"], ["math", "html", "thvnhmtng"], ["thanhminh", "arteriosclerosis"]]

print("----build index-----")
Ii = build_index(Wi[2], SK)

print("----build trapdoor----")

print("----build trapdoor 1----")

TQj = trapdoor0(Qj, SK)
print("----build trapdoor 2----")

TQjs = trapdoorS(Qj, SK)

print("----Search -------")


print(search(Ii, TQj, "AND"))
print(searchS(Ii, TQjs, "AND"))
