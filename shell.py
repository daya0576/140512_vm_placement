import os

file_dir = "input/vm_flow_matrix/"
#file_list = os.listdir(file_dir)
file_list = ["2Partitions@5percent.data"]

#methods = [" -h "]
methods = [" -a ", " -m ", " -n ", " -h ", " -b ", " -z "]


for filename in file_list:
    print filename + "\ting....."

    for method in methods:
        print "\nmethod: " + method
        cmd1 = "h:/PYTHON26/python.exe 1_MC_BT_algorithm.py " + file_dir + filename + method + " > 1_MC_BT_result/test1.txt" 
        #  + " > test/" + filename +"_test1.txt" 
        os.system(cmd1)
        
        cmd2 = "h:/PYTHON26/python.exe 2_BF_algorithm.py " + file_dir + filename
        # + " > test/" + filename +"_test2.txt"
        os.system(cmd2)


file_name = "2Partitions@5percent"
print "\nmethod: -matlab"
cmd12 = "h:/PYTHON26/python.exe 1_handle_cluster_result.py " + file_name + " > 1_MC_BT_result/test1.txt" 
#  + " > test/" + filename +"_test1.txt" 
os.system(cmd12)

cmd2 = "h:/PYTHON26/python.exe 2_BF_algorithm.py " + file_dir + file_name + ".data"
# + " > test/" + filename +"_test2.txt"
os.system(cmd2)







