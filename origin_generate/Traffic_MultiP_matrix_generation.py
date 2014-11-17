import numpy as np
import random as rnd
import math

def GenTrafficMatrix(N=1024,r=0,pNum=2,percentage=3):
    matrix = np.zeros((N,N))
    mean = 0
    stdvar = 1
    li=[]

    # random traffic
    for rndx in range(0,r):
        i = rnd.randint(0,(N-1))
        j = rnd.randint(0,i)
        matrix[i,j] = rnd.random()

    # Gen partitions ,default 1 partition
    for i in range(0,pNum):
        M = math.floor(percentage * N / 100 )    
        if li:
            for I in range(0,len(li)):
                pi = rnd.randint(0,(N-M))
                pj = rnd.randint(0,(N-M))
                c = ( li[I][0] < pi and pi < li[I][0] + li[I][2] and li[I][1] < pj and pj < li[I][1]+li[I][2] )
                while c:
                    pi = rnd.randint(0,(N-li[I][2]))
                    pj = rnd.randint(0,pi)
                    c = ( li[I][0] < pi and pi < li[I][0] + li[I][2] and li[I][1] < pj and pj < li[I][1]+li[I][2] )
        else:
            pi = rnd.randint(0,(N-M))
            pj = rnd.randint(0,pi)

        li.append((pi,pj,M))
        partition = np.random.normal(mean, stdvar, (M,M))
        for i in range(0,M):
            for j in range(0,M):
                partition[i,j]=abs(partition[i,j])
        matrix[pi:(pi+M),pj:(pj+M)] = partition

    matrix = matrix+matrix.T
    di = np.diag_indices(N)
    matrix[di]=0
    return  matrix

def WriteMatrixIntoFile(matrix,pNum,percentage):
    fileName = "data//"+str(pNum)+"Partitions@"+str(percentage)+"percent.data"
    with open(fileName, mode = "w") as fout:
        for row in matrix:
            for ele in row:
                if ele==0:
                    ele = "0"
                else:
                    ele = str("%.1f"%ele)
                fout.write(str(ele)+"\t")
            fout.write("\n")

#OUTPUT SEG
for pNum in range(2,3):
    print("pNum="+str(pNum))
    for percentage in [5,15,25,35]:
        print("percentage="+str(percentage))
        WriteMatrixIntoFile(GenTrafficMatrix(1024,0,pNum,percentage),pNum,percentage)
        
        
        
        
        
        
        

