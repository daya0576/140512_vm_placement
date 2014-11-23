import os
import sys

file_dir = "input/vm_flow_matrix/"
file_list = [file[0:-5] for file in os.listdir(file_dir)]
#file_list = ["2Partitions@5percent"]
#for filename in file_list:
#    print "\'"+filename+"\'",


#methods = [" -h "]
methods = [" -a ", " -m ", " -n ", " -h ", " -b ", " -z "]


for filename in file_list:
    print filename + "\ting....."
    
    for method in methods:
        print "method: " + method
        cmd1 = "h:/PYTHON26/python.exe 1_MC_BT_algorithm.py " + file_dir + filename + ".data" + method + " > 1_MC_BT_result/test1.txt" 
        #  + " > test/" + filename +"_test1.txt" 
        os.system(cmd1)
        
        cmd2 = "h:/PYTHON26/python.exe 2_BF_algorithm.py " + file_dir + filename + ".data"
        # + " > test/" + filename +"_test2.txt"
        os.system(cmd2)

    for criterion in ['_ncut', '_ncc', '_rcut', '_rcc']:
        
        print "method: -matlab " + criterion
        cmd12 = "h:/PYTHON26/python.exe 1_handle_cluster_result.py " + filename + criterion + " > 1_MC_BT_result/test1.txt" 
        #  + " > test/" + filename +"_test1.txt" 
        os.system(cmd12)
        
        cmd2 = "h:/PYTHON26/python.exe 2_BF_algorithm.py " + file_dir + filename + ".data"
        # + " > test/" + filename +"_test2.txt"
        os.system(cmd2)
    
    print "Done. "







