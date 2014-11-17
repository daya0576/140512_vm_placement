import numpy as np
import random as rnd
import math
import os,sys

def GenTrafficMatrix(sourceFile,PNNum=64):
    srcMatrix = ReadFileIntoMatrix(sourceFile)
    dstMatrix = np.zeros((PNNum,PNNum))
    step = 1024 / PNNum

    # Gen Matrix
    for i in range(0,1024):
        for j in range(i,1024):
            ele=float(srcMatrix[i][j])
            dstMatrix[(math.floor(i / step))][(math.floor(j / step))] += ele
    dstMatrix = dstMatrix + dstMatrix.T
    di = np.diag_indices(PNNum)
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
for PNNum in [128]:
    print("")
    for sourceFile in os.listdir("data\\"):
        print("start processing file:" + sourceFile + " with PN number:" + str(PNNum))
        dstFile = str(PNNum) + "PN" + "_" + sourceFile
        WriteMatrixIntoFile(GenTrafficMatrix("data\\" + sourceFile,PNNum),dstFile)

