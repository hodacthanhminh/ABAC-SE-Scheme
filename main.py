# libs
import numpy as np
# constant
from CONSTANT import *
# function
import knn
from genkey import *
from buildindex import *
from trapdoor import *

SK = genkey(k)


(sk,kF,Dummies,Primes) = SK  
print(Primes)
(M1,M2,S) = sk

Wi =[["thanhminhabcxd","thplhmiwh","temp"],["math","html","thanhminh"],["thanhminh"]]
Qj =["thanhmin****xd"]

TQj= trapdoor(Qj,SK)
for x,val in enumerate(Wi):
    print("------ Search W_{} with TQj----------".format(x))
    Ii= build_index(val,SK)
    query_result = []
    search_matrix = knn.Search(Ii, TQj)
    result_query=[]
    or_column = 0
    and_column = 1
    result_abs = np.round_(abs(np.int64(search_matrix) - np.float64(search_matrix)),decimals=6)
    print(">>abs", result_abs)
    for i in result_abs:
        row_temp =[]
        or_row = 0
        and_row = 0
        for j in i:
            if ((1 >= j >= 0.99545) or (0 <= j <= 0.00045)): 
                row_temp.append(1)
                or_row = or_row or 1
                and_row = and_row or 1
            else: 
                row_temp.append(0)
                or_row = or_row or 0
                and_row = and_row or 0
        result_query.append(row_temp)
        or_column = or_column or or_row
        and_column = and_column and and_row
    print(">> query",result_query," OR query:", bool(or_column), "| AND query", bool(and_column) )










