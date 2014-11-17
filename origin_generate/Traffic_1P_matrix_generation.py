import numpy as np
import random as rnd

def GenTrafficMatrix(percentage=5):
    N = 64
    r=100
    matrix = np.zeros((N,N))

    for rndx in xrange(0,r):
        i = rnd.randint(0,(N-1))
        j = rnd.randint(0,i)
        matrix[i,j] = rnd.random()

    M = percentage * N / 100 
    mean = 0
    stdvar = 1
    pi = rnd.randint(0,(N-M))
    pj = rnd.randint(0,(N-M))
    partition = np.random.normal(mean, stdvar, (M,M))
    for i in xrange(0,(M)):
        for j in xrange(0,M):
            if i > j:
                partition[i,j]=0

    matrix[pi:(pi+M),pj:(pj+M)] = partition

    matrix=matrix+matrix.T
    di=np.diag_indices(N)
    matrix[di]=0
    return  matrix

def WriteMatrixIntoFile(matrix,percentage):
    fileName = "1Partition@"+str(percentage)+".data"
    with open(fileName, mode = "w") as fout:
        for row in matrix:
            for ele in row:
                fout.write(str(ele)+"\t")
            fout.write("\n")

for h in [5,15,25,35]:
    WriteMatrixIntoFile(GenTrafficMatrix(h),h)