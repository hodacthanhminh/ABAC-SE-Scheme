from numpy import np

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
