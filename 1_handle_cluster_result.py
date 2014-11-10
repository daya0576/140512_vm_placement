import sys
print "-------------algorithm1---------------"
#mat_result_file = "input/cluster_result/" + sys.argv[1] + "_1024.data"
mat_result_file = "input/cluster_result/test141106.data"
print mat_result_file

def write_lines_to_file(result_G_nodes, filename):
    file_object = open(filename, 'w')
    try:
        for result in result_G_nodes:
            result = str(result) + " "
            file_object.write(result)
        #simplejson.dump(result_G_nodes, file_object)
    finally:
        file_object.close()

def read_lines_from_file(filename):
    file_object = open(filename)
    try:
        list_of_all_the_lines = file_object.readlines()
    finally:
        file_object.close()

    list_new = []
    for line in list_of_all_the_lines:
        line = line.split(',')
        line_int = [int(str1) for str1 in line]
        list_new.append(line_int)
        #print line_int 

    return list_new
    
def handle(cluster_result):
    cluster_result.insert(0, [1]*len(cluster_result[0]));
    binary_result = ["1"]*len(cluster_result)
    #print cluster_result
    for single_result in cluster_result:
        k = cluster_result.index(single_result)
        if k == 0:continue

        cut_node = 0
        for (index, single_node) in enumerate(single_result):
            pre_node = cluster_result[k-1][index]
            if single_node != pre_node:
                cut_node = pre_node
                binary_result[index] += "2"
        for (index, single_node) in enumerate(single_result): 
            pre_node = cluster_result[k-1][index]  
            #print pre_node, single_node, cut_node       
            if cut_node == pre_node and cut_node == single_node:
                binary_result[index] += "1"
        
    return binary_result

def next_lower(a, b):
    length1 = len(a if len(a) < len(b) else b);
        
    for i in range(length1):
        if int(b[i]) < int(a[i]):
            return True
        elif int(b[i]) > int(a[i]):
            return False
   
def sort_nodes(binary_result):
    vms =  range(len(binary_result))
    #vms = [1, 2, 3, 4]
    for i in range(len(vms)):
        for j in range(len(vms)-i-1):
            if next_lower(binary_result[j], binary_result[j+1]):
                vms[j], vms[j + 1] = vms[j + 1], vms[j]
                binary_result[j] , binary_result[j+1] = binary_result[j+1] , binary_result[j]
    print binary_result
        #print vms
    return vms
     
def test_matlab_result():
    print "sort_by_cluster(matlab)"
    file_lists = read_lines_from_file(mat_result_file) 
    num_of_cuts = len(file_lists[0]);
    cluster_result = [];
    for i in range(num_of_cuts):
        cluster_result.append([int(list1[i]) for list1 in file_lists]);
        
    binary_result = handle(cluster_result)
    
    result_G_nodes = sort_nodes(binary_result);
    print result_G_nodes

    write_lines_to_file(result_G_nodes, "1_MC_BT_result/nodes_result.data")
    
    
if __name__ == "__main__" :
    test_matlab_result()
    
    

    
    
    