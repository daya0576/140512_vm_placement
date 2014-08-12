import os

file_dir = "input/vm_flow_matrix/"
#file_list = os.listdir(file_dir)
file_list = ["2Partitions@5percent.data"]

for filename in file_list:
    print filename + "\ting....."
    cmd1 = "h:/PYTHON26/python.exe 1_MC_BT_algorithm.py " + file_dir + filename
    #  + " > test/" + filename +"_test1.txt" 
    os.system(cmd1)
    
    cmd2 = "h:/PYTHON26/python.exe 2_BF_algorithm.py " + file_dir + filename
    # + " > test/" + filename +"_test2.txt"
    os.system(cmd2)


