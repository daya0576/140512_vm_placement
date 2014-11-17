import numpy as np
import random as rnd
import math
import os,sys

def GenTrafficMatrix(sourceFile,srvNum=50):
    srcMatrix = ReadFileIntoMatrix(sourceFile)
    dstMatrix = np.zeros((srvNum,srvNum))
    node =1024

    u = node/srvNum
    step = np.random.poisson(u,srvNum)
    count = 0
    for s in step:
        count += s
    delta = math.floor((count - node) / srvNum)
    count=0
    for i in range(0,srvNum):
        step[i] -= delta
        count += step[i]
    while count > node-1:
        i = rnd.randint(0,srvNum-1)
        step[i] -= 1
        count -= 1
    while count < node-1:
        i = rnd.randint(0,srvNum-1)
        step[i] += 1
        count +=1

    ref=step
    for i in range(0,srvNum):
       if i >0 :
         ref[i]+= ref[i-1]

    for i in range(0,srvNum):
        ref[i] += -1

    # Gen Matrix
    dstMatrix=np.zeros((srvNum,srvNum))
    x=0
    for i in range(0,node):
        y=0
        if (x < srvNum and y < srvNum):
            for j in range(i,node):
                if (x < srvNum and y < srvNum):
                    ele=float(srcMatrix[i][j])
                    dstMatrix[x][y] += ele
                    if j == ref[y]:
                        y+=1
            if i == ref[x]:
                x+=1

    dstMatrix = dstMatrix + dstMatrix.T
    di = np.diag_indices(srvNum)
    dstMatrix[di] = 0
    return  dstMatrix


def ReadFileIntoMatrix(file):
    matrix=[]
    with open(file, mode = "r") as fin:
        lines = fin.readlines()
        for row in lines:
            matrix.append((row.split('\n'))[0].split("\t"))
    fin.close
    return matrix


def WriteMatrixIntoFile(matrix,fileName):
    with open(fileName, mode = "w") as fout:
        for row in matrix:
            for ele in row:
                fout.write(str(ele)+"\t")
            fout.write("\n")
    fout.close


#OUTPUT SEG
for srvNum in [50,100,200]:
    print("")
    for sourceFile in os.listdir("data\\"):
        print("start processing file:" + sourceFile + " with services number:" + str(srvNum))
        dstFile = str(srvNum) + "services" + "_" + sourceFile
        WriteMatrixIntoFile(GenTrafficMatrix("data\\" + sourceFile,srvNum),dstFile)

