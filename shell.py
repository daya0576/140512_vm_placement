import os

file_dir = "input/vm_flow_matrix/"
file_list = os.listdir(file_dir)


for filename in file_list:
    print filename + "\ting....."
    cmd1 = "python 1_MC_BT_algorithm.py " + file_dir + filename + " > test/" + filename +"_test1.txt"
    os.system(cmd1)
    
    cmd2 = "python 2_BF_algorithm.py " + file_dir + filename + " > test/" + filename +"_test2.txt"
    os.system(cmd2)
