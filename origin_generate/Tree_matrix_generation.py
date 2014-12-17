def GenCostMatrixFatTree():
    N, k = 1024, 16
    matrix = []
    for i in range(1, N + 1):
        rowVec = []
        for j in range(1, N + 1):
            if i == j:
                rowVec.append(0)
            elif 2 * i // k == 2 * j // k:
                rowVec.append(1)
            elif 2 * i // k != 2 * j // k and 4 * i // (k * k) == 4 * j // (k * k):
                rowVec.append(3)
            elif 4 * i // (k * k) != 4 * j // (k * k):
                rowVec.append(5)
            else:
                print("generation error")
                return
        matrix.append(rowVec)
 
    return matrix
 
def GenCostMatrixTree():
    N, p0, p1 = 1024, 16, 8
    matrix = []
    for i in range(1, N + 1):
        rowVec = []
        for j in range(1, N + 1):
            if i == j:
                rowVec.append(0)
            elif i // p0 == j // p0:
                rowVec.append(1)
            elif i // p0 != j // p0 and i // (p0 * p1) == j // (p0 * p1):
                rowVec.append(3)
            elif i // (p0 * p1) != j // (p0 * p1):
                rowVec.append(5)
            else:
                print("generation error")
                return
 
        matrix.append(rowVec)
 
    return matrix
 
def WriteMatrixIntoFile(matrix,fileName):
    with open(fileName, mode = "w", encoding = "utf-8") as fout:
        for row in matrix:
            for ele in row:
                fout.write(str(ele))
                fout.write(" ")
            fout.write("\n")

WriteMatrixIntoFile(GenCostMatrixFatTree(),"CostMatrix_FatTree.data")
WriteMatrixIntoFile(GenCostMatrixTree(),"CostMatrix_Tree.data")

