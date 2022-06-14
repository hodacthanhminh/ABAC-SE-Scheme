# libs
import numpy as np
# class/funcs
from .knn import KNN


def handle_result(result):
    result_abs = [[round(abs(int(x) - x), 4) for x in y] for y in result]
    result_query = []
    for i in result_abs:
        row_temp = []
        for j in i:
            if (j == 1 or j == 0):
                row_temp.append(1)
            else:
                row_temp.append(0)
        result_query.append(row_temp)
    return np.transpose(result_query)


def handle_searchS_sum(result):
    sum_matrix = []
    for r_k in result:
        sum_row = []
        for r_kl in r_k:
            sum = 0
            for num in r_kl:
                sum += num
            sum_row.append(sum)
        sum_matrix.append(sum_row)
    return sum_matrix


def and_query(matrix):
    result = 1
    for i in matrix:
        row = 0
        for j in i:
            row = row or j
        result = result and row
    return result


def or_query(matrix):
    result = 0
    for i in matrix:
        row = 0
        for j in i:
            row = row or j
        result = result or row
    return result


class Search:
    def __init__(self, andQ: bool, basic: bool):
        self.andQ = andQ
        self.basic = basic

    def calculate(self, result_binary):
        if (self.andQ):
            return and_query(result_binary)
        else:
            return or_query(result_binary)

    def search_result(self, Ii, TQj):
        search_matrix = KNN.Search(Ii, TQj)
        if (self.basic):
            result_binary = handle_result(search_matrix)
        else:
            sum_matrix = handle_searchS_sum(search_matrix)
            result_binary = handle_result(sum_matrix)
        return self.calculate(result_binary)
