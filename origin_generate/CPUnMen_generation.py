import numpy as np
import random as rnd
import math

def GenDistribution(N=128,pcpu=25,pmen=60,stdvar=1):
    cpu = np.zeros(N)
    men = np.zeros(N)
    mean = 0
    #stdvar = 1
    cpumean=pcpu
    memmean=pmen

    # random loads
    a = np.random.normal(cpumean, stdvar, (15240))
    b = [a[i] for i in range(0, len(a) - 1) if  ( a[i] >= 0 and (a[i] <= 1 and a[i]<=2*cpumean) )]
    
    cpu =b[:N]
    c = np.random.normal(memmean, stdvar, (15240))
    d = [c[i] for i in range(0, len(c) - 1) if  ( c[i] >= 0 and (c[i] <= 1 and c[i]<=2*memmean) )]
    men = d[:N]
    data=cpu,men
    return  data

def WriteIntoFile(data,fileName,N):
    a=data[0]
    b=data[1]
    with open(fileName, mode = "w") as fout:
        for i in range(N):
            fout.write(str(a[i])+"\t")
            fout.write(str(b[i])+"\t")
            fout.write("\n")

#OUTPUT SEG
for node in [64,256,1024]:
    for pcpu in [0.20,0.30,0.40,0.50]:
        for pmen in [0.20,0.30,0.40,0.50]:
            for stdvar in [0.5,1,2]:
                fileName="Node"+str(node)+"_cpu"+str(pcpu)+"_men"+str(pmen)+"_stdvar"+str(stdvar)
                print("OUTPUT:"+fileName)
                WriteIntoFile(GenDistribution(node,pcpu,pmen,stdvar),fileName,node)
