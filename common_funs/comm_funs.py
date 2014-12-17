import networkx as nx  

def read_lines_from_file(filename):
    with open(filename) as f:
        list_of_all_the_lines = f.readlines()
            
    return lines_to_list(list_of_all_the_lines)

def lines_to_list(list_of_all_the_lines):
    list_new = []
    for line in list_of_all_the_lines:
        line = line.strip('\n')
        line = line.strip('\t')
        line = line.split()
        list_new.append(line)

    return list_new

def file_lists_to_G_lists(file_lists):
    lines_new = []
        
    for i, line in enumerate(file_lists):
        for j, vm in enumerate(line):
            vm = float(vm)
            if(vm > 0 and j >= i):
                vm_list_tmp = []
                vm_list_tmp.append(i)
                vm_list_tmp.append(j)                
                vm_list_tmp.append(vm)                
                lines_new.append(vm_list_tmp)
                    
    return lines_new

def get_activity_nodes(vm_flow_file):
    G_origin = nx.Graph()
    file_lists = read_lines_from_file(vm_flow_file)    
    G_origin_lists = file_lists_to_G_lists(file_lists)
    G_origin.add_weighted_edges_from(G_origin_lists)
    activity_nodes = G_origin.nodes()
    
    return activity_nodes