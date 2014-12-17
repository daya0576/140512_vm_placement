# -*- coding: utf-8 -*- 

import os
import sys
#sys.exit()

def file_print(filename, text):
    with open(filename, 'a') as f:
        f.write(text + "\n")

pythonPath = "h:/PYTHON26/python.exe"
file_dir = "input/vm_flow_matrix/"
#file_list = [file[0:-5] for file in os.listdir(file_dir) 
#             if ("@5percent" in file or "@15percent" in file)]
file_list = ["1Partitions@15percent"]

methodDetails = unicode("-a: vm按序号排列， 子图分开\n" + \
                        "-m: MC_BF\n" + \
                        "-n: vm nodes权重 \n" + \
                        "-h: sort_weight_by(Gomory Hu Tree)\n" + \
                        "-b: sort_weight_by_both(G_hu, G_origin)\n " + \
                        "-z: zcj method\n" ,"utf8")
                
#methods = [" -m "]
methods = [" -a ", " -m ", " -n ", " -h ", " -b "]
pmTypes = [#"Node1024_cpu0.5_men0.3_stdvar1", 
           #"Node1024_cpu0.5_men0.5_stdvar1", 
           "Node1024_cpu0.2_men0.2_stdvar1"]

for filename in file_list:
    fileLoc = file_dir + filename + ".data "
    print fileLoc
    #sys.exit()
    resultLoc = "test/" + filename +"_test1.txt"
    print filename + "\ting....." 
    file_print(resultLoc, methodDetails)
    file_print(resultLoc, filename + "\ting.....")
    
    for pmType in pmTypes:
        pmTypeLoc = "input/vm_cost/" + pmType
        print pmType + "\ting....." 
        file_print(resultLoc, "\n" + pmType + "\ting.....")
        
        for method in methods:
            print "method: " + method
            file_print(resultLoc, "method: " + method)
            cmd1 = pythonPath + " 1_MC_BT_algorithm.py " + fileLoc + " " + method
            os.system(cmd1)
            
            cmd2 = pythonPath + " 2_BF_algorithm.py " + fileLoc + " " + pmTypeLoc + " >> " + resultLoc
            os.system(cmd2)
    
        for criterion in ['_ncut', '_ncc', '_rcut', '_rcc']:
            print "method: -matlab " + criterion
            file_print(resultLoc, "method: -matlab " + criterion)
            
            cmd12 = pythonPath + " 1_handle_cluster_result.py " + \
                filename + criterion + " >> 1_MC_BT_result/test1.txt" 
            os.system(cmd12)
            
            cmd2 = pythonPath + " 2_BF_algorithm.py " + fileLoc + " " +  pmTypeLoc + " >> " + resultLoc
            os.system(cmd2)
    
    file_print(resultLoc, "Done. \n")







