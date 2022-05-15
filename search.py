import numpy as np
from buildindex import *
from knn import *

Wi =[["thanhminh","thplhmiwh","temp"],["math","html","thvnhmtng"],["thanhminh","arteriosclerosis"]]

def handleResult(result):
    result_abs = np.round_(abs(np.int64(result) - result),decimals=6)
    result_query = []
    for i in result_abs:
        row_temp =[]
        for j in i:
            if ((1 >= j >= 0.99545) or (0 <= j <= 0.00045)): 
                row_temp.append(1)
            else: 
                row_temp.append(0)
        result_query.append(row_temp)
    return np.transpose(result_query)

def andQuery(matrix):
    result = 1
    for i in matrix:
        row = 0
        for j in i:
            row = row or j
        result = result and row
    return result

def orQuery(matrix):
    result = 0
    for i in matrix:
        row = 0
        for j in i:
            row = row or j
        result = result or row
    return result


def search(TQj, SK, type = "AND"):
    doc_match = []
    for i,val in enumerate(Wi):
        print("----------- Doc {}-----------".format(i))
        print("Keyword:",val)
        Ii = build_index(val, SK)
        search_matrix = knn.Search(Ii, TQj)
        sum_matrix = []
        for r_k in search_matrix:
            sum_row = []
            for r_kl in r_k:
                sum = 0
                for num in r_kl:
                    sum+=num
                sum_row.append(sum)
            sum_matrix.append(sum_row)
        print(sum_matrix)
        result_binary=handleResult(sum_matrix)
        if (type == "AND" and andQuery(result_binary)) or (type == "OR" and orQuery(result_binary)): 
            print("search match")
            doc_match.append(i)
        else:
            print("not match")
    return doc_match

