from operator import invert
from genkey import *
from hash import *
import numpy as np

key_length = 2

secret_key = genkey(key_length)

([M1,M2,S],kF,dummy,prime) = secret_key

p = np.array([1/3,1/7])
q = np.array([33,7])

print(">> sk[S]", S)
print(">> sk[M1]", M1)
invert_M1 = np.linalg.inv(M1).reshape([key_length,key_length])
transpose_M1 = np.transpose(M1).reshape([key_length,key_length])
print(">> inverted sk[M1]",invert_M1)
print(">> transpose sk[M1]",transpose_M1)
print(">> inner product M_T M_1:",np.inner(transpose_M1,invert_M1))
print("------------")
print(">> sk[M2]", M2)
invert_M2 = np.linalg.inv(M2).reshape([key_length,key_length])
transpose_M2 = np.transpose(M2).reshape([key_length,key_length])
print(">> inverted sk[M2]",invert_M2)
print(">> transpose sk[M2]",transpose_M2)




def splitIndex(arr):
    arr_a = []
    arr_b = []
    for i,vals in enumerate(S):
        if vals == 0:
            vals_a = vals_b = arr[i]
            arr_a.append(vals_a)
            arr_b.append(vals_b)

        else: 
            vals_a = 0.5*arr[i]+0.2
            vals_b = 0.5*arr[i]-0.2
            arr_a.append(vals_a)
            arr_b.append(vals_b)
    return [arr_a,arr_b]

def splitQuery(arr):
    arr_a = []
    arr_b = []
    for i,vals in enumerate(S):
        if vals == 1:
            vals_a = vals_b = arr[i]
            arr_a.append(vals_a)
            arr_b.append(vals_b)

        else: 
            vals_a = 0.5*arr[i]+0.1
            vals_b = 0.5*arr[i]-0.1
            arr_a.append(vals_a)
            arr_b.append(vals_b)
    return [arr_a,arr_b]

# index

p_split = splitIndex(p)
print(">>p_split",p_split)

p_a = np.matmul(M1,p_split[0])
p_b = np.matmul(M2,p_split[1])
print(">> p(p_a,p_b):", p_a,"-",p_b)

print("-------------------")
q_split = splitQuery(q)
print(">>q_split", q_split)
q_a = np.matmul(np.transpose(invert_M1),q_split[0])
q_b = np.matmul(np.transpose(invert_M2),q_split[1])
print(">> q(q_a,q_b):",q_a,"-",q_b)
print("q_a shape:",np.shape(q_a))
print("q_b shape:",np.shape(q_b))

print(">>inner pai - qai:", np.inner(p_a,q_a))
print(">>inner pbi - qbi:", np.inner(p_b,q_b))
print(">>inner sum", np.inner(p_b,q_b) + np.inner(p_a,q_a))
print(">> inner p - q:", np.inner(p,q))







