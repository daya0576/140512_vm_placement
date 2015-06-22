# -*- coding: utf-8 -*- 

import os
import sys
import time
local_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
local_time = str(time.strftime('_%H:%M',time.localtime(time.time())))

# sys.exit()

def file_print(filename, text, line = True):
    with open(filename, 'a') as f:
        if line is True:
            f.write(text + "\n")
        else: 
            f.write(text)
        
def file_cls(filename, text):
    with open(filename, 'w') as f:
        f.write(text + "\n")

#pythonPath = "C:\Python26\Python26/python.exe"
pythonPath = "h:/PYTHON26/python.exe"

file_dir = "input/vm_flow_matrix/"
# file_list = [file[0:-5] for file in os.listdir(file_dir) 
#              if ("@5percent" in file or "@15percent" in file)]
file_list = ["1Partitions@5percent"]

methodDetails = unicode("-a: vm按序号排列， 子图分开\n" + \
                        "-m: MC_BF\n" + \
                        "-n: vm nodes权重 \n" + \
                        "-h: sort_weight_by(Gomory Hu Tree)\n" + \
                        "-b: sort_weight_by_both(G_hu, G_origin)\n " + \
                        "-z: zcj method\n" ,"utf8")
                
# methods = []
# methods = [" -a ", " -m ", " -n ",  " -b "]
methods = [" -a ", " -h "]
pmTypes = [#"Node1024_cpu0.5_men0.3_stdvar1", 
           #"Node1024_cpu0.5_men0.5_stdvar1", 
           "Node1024_cpu0.2_men0.2_stdvar1"]

dir_name = "test/" + local_date
if not os.path.isdir(dir_name):
    os.makedirs(dir_name)
for filename in file_list:
    fileLoc = file_dir + filename + ".data "
    resultLoc = dir_name + "/" + filename +"_test_2.txt"
    print filename + "\ting....." 
    file_cls(resultLoc, methodDetails)
    file_print(resultLoc, filename + "\ting.....")
    
    for pmType in pmTypes:
        pmTypeLoc = "input/vm_cost/" + pmType
        print pmType + "\ting....." 
        file_print(resultLoc, "\n" + pmType + "\ting.....")
        
        for method in methods:
            print "\nmethod: " + method
            file_print(resultLoc, "\nmethod: " + method)
            cmd1 = pythonPath + " 1_MC_BT_algorithm.py " + fileLoc + " " + method
            os.system(cmd1)   
            file_print(resultLoc, "\nBest fit: \n", False)
            cmd2 = pythonPath + " 2_BF_algorithm.py " + filename + " " + pmTypeLoc + " best " + resultLoc
            os.system(cmd2)
            cmd4 = pythonPath + " 3_solution_analyze.py " + filename + " " +  resultLoc
            print resultLoc
            os.system(cmd4)
            
            file_print(resultLoc, "tabu search: ", False)
            cmd3 = "tabou_qap2_vmmove.exe " + fileLoc + " " + pmTypeLoc + " " + resultLoc# + " >> " + resultLoc
            print cmd3
            #os.system(cmd3) 
            os.system(cmd4)
            
            file_print(resultLoc, "\nFirst fit: \n", False)
            cmd2 = pythonPath + " 2_BF_algorithm.py " + filename + " " + pmTypeLoc + " first " + resultLoc
            os.system(cmd2)
            os.system(cmd4)
            
            
            file_print(resultLoc, "tabu search: ", False)
            #os.system(cmd3) 
            os.system(cmd4)
    
        #for criterion in ['_ncut', '_ncc', '_rcut', '_rcc']:
        for criterion in ['_ncc']:
            print "\nmethod: -matlab " + criterion
            file_print(resultLoc, "\nmethod: -matlab " + criterion)
            
            cmd12 = pythonPath + " 1_handle_cluster_result.py " + \
                filename + criterion + " "  + fileLoc + \
                " >> 1_MC_BT_result/test1.txt" 
            os.system(cmd12)
            file_print(resultLoc, "\nBest fit: \n", False)
            cmd2 = pythonPath + " 2_BF_algorithm.py " + filename + " " +  pmTypeLoc + " best " + resultLoc
            print cmd2
            os.system(cmd2)
            os.system(cmd4)
            
            file_print(resultLoc, "tabu search: ", False)
            cmd3 = "tabou_qap2_vmmove.exe " + fileLoc + " " + pmTypeLoc + " " + resultLoc# + " >> " + resultLoc
            print cmd3
            #os.system(cmd3)
            os.system(cmd4) 
            
            file_print(resultLoc, "\nFirst fit: \n", False)
            cmd2 = pythonPath + " 2_BF_algorithm.py " + filename + " " + pmTypeLoc + " first " + resultLoc
            os.system(cmd2)
            os.system(cmd4)
            
            file_print(resultLoc, "tabu search: ", False)
            #os.system(cmd3) 
            os.system(cmd4)
    
    file_print(resultLoc, "Done. \n")







