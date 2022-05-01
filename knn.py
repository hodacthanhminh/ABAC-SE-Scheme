import numpy as np

def genInvertedMatrix(k):
    while True:
        Matrix = np.random.randint(1,4,[k,k])
        if np.linalg.matrix_rank(Matrix) == k:
             return Matrix

def key(k): 
    M1 = genInvertedMatrix(k)
    M2 = genInvertedMatrix(k)
    S = np.random.randint(2,size=k)

    return [M1,M2,S]

def EncI(p,sk):
    [M1,M2,S] = sk
    p_a=[]
    p_b=[]
    r = np.random.randint(0,1)
    for i,value in enumerate(S):
        val_a = val_b = 0
        if value == 0:
            val_a = val_b = p[i]
        else:
            val_a = p[i]*0.5 + r 
            val_b = p[i]*0.5 + r 
        p_a.append(val_a)
        p_b.append(val_b)
    p_encrypt_a = np.matmul(M1,p_a)
    p_encrypt_b = np.matmul(M2,p_b)

    return [p_encrypt_a, p_encrypt_b]

def EncQ(q,sk):
    [M1,M2,S] = sk
    q_a=[]
    q_b=[]
    r = np.random.randint(0,1)
    invert_M1 = np.linalg.inv(M1)
    invert_M2 = np.linalg.inv(M2)
    for i,value in enumerate(S):
        val_a = val_b = 0
        if value == 1:
            val_a = val_b = q[i]
        else:
            val_a = q[i]*0.5 + r 
            val_b = q[i]*0.5 + r 
        q_a.append(val_a)
        q_b.append(val_b)
    q_encrypt_a = np.matmul(np.transpose(invert_M1),q_a)
    q_encrypt_b = np.matmul(np.transpose(invert_M2),q_b)

    return [q_encrypt_a, q_encrypt_b]

def Search(I,Q): 
    [p_ea, p_eb] = I
    [q_ea, q_eb] = Q

    return np.inner(q_ea,p_ea) + np.inner(q_eb,p_eb)

    
    

