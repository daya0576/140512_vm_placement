import networkx as nx  
import xlwt

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

def read_list_from_file(filename):
    with open(filename) as f:
        list_of_all_the_lines = f.readline()
        line = list_of_all_the_lines.split()    
    return line

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

def write_line_to_file(result_G_nodes, filename):
    with open(filename, 'w') as f:
        for result in result_G_nodes:
            result = str(result) + " "
            f.write(result)
            
def write_str_to_file(content, filename):
    with open(filename, 'a') as f:
        f.write(content)
        
        
def list2xls(input_name, output_name):   
    fileList = read_list_from_file(input_name)
    #print fileList
    
    wfile = xlwt.Workbook()
    table = wfile.add_sheet("1")
    
    for k, num in enumerate(fileList):
        table.write(0, k, str(num))
        if k > 50:
            break
    wfile.save(output_name)
        
           
         
        
        