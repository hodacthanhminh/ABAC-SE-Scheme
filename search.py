import numpy as np
from buildindex import *
from knn import *

Wi = [["thanhminh", "thplhmiwh", "temp"], ["math", "html", "thvnhmtng"], ["thanhminh", "arteriosclerosis"]]


def handleResult(result):
    result_abs = [[round(abs(int(x) - x), 4) for x in y] for y in result]
    print(">> result", result_abs)
    result_query = []
    for i in result_abs:
        row_temp = []
        for j in i:
            if (j == 1 or j == 0):
                row_temp.append(1)
            else:
                row_temp.append(0)
        result_query.append(row_temp)
    print(result_query)
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


def search(Ii, TQj, type="AND"):
    search_matrix = knn.Search(Ii, TQj)
    result_binary = handleResult(search_matrix)
    if (type == "AND" and andQuery(result_binary)) or (type == "OR" and orQuery(result_binary)):
        return "search match"
    else:
        return "not match"


def searchS(Ii, TQj, type="AND"):
    search_matrix = knn.Search(Ii, TQj)
    sum_matrix = handleSearchSSum(search_matrix)
    print(sum_matrix)
    result_binary = handleResult(sum_matrix)
    if (type == "AND" and andQuery(result_binary)) or (type == "OR" and orQuery(result_binary)):
        return "search match"
    else:
        return "not match"
