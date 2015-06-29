
import sys


def read_line_from_file(filename):
    with open(filename) as f:
        line_result = f.readlines()
    
    line = line_result[0].strip('\n').split(' ')
    line_new = [int(i) for i in line if len(i)>0]
    
    return line_new

def lines_to_list(list_of_all_the_lines):
    list_new = []
    for line in list_of_all_the_lines:
        line = line.strip('\n')
        line = line.replace('\t', " ")
        line = line.split()
        line_new = []
        for num in line:
            num = float(num)
            line_new.append(num)
        list_new.append(line_new)
        
    return list_new

def read_matrix(filename):
    with open(filename) as file_object:
        lines = file_object.readlines()
    return lines_to_list(lines)

def write_str_to_file(content, filename):
    with open(filename, 'a') as f:
        f.write(content)

def compute_mul(VM_flow_matrix, PMlist_distance, solution):
    final_result = 0
    flow_sum = 0            
    for VM1 in xrange(1024):
        for VM2 in xrange(VM1):
            flow = VM_flow_matrix[VM1][VM2]
            distance = PMlist_distance[solution[VM1]][solution[VM2]]
            if flow > 0 and distance > 0:
                flow_sum += 1 
                #print final_result, ' += ', distance, ' * ',  flow
                final_result += distance * flow

    return final_result    

solution = read_line_from_file("test/mapping_result/solution.data")

vm_flow_file = sys.argv[1]
vm_flow_file_loc = "input/vm_flow_matrix/" + vm_flow_file + ".data"
pm_dist_file = "input/pm_distance/pm_distanc_1024.data"
resultLoc = sys.argv[2]

PMlist_distance = read_matrix(pm_dist_file)
VM_flow_matrix = read_matrix(vm_flow_file_loc)


'''compute (distace * flow)'''
final_result = compute_mul(VM_flow_matrix, PMlist_distance, solution)
print '  1. compute (distace * flow): ' + str(final_result)
write_str_to_file("sum(distace * flow):" + str(final_result) + "\n", resultLoc)

''' Core/Aggregate/Edge ''' 
core_sum = 0
agge_sum = 0
edge_sum = 0
vm_dis_sum = 0
dis_count = 0
for i in range(1024):
    for j in range(i):
        if VM_flow_matrix[i][j] > 0:
            vm_dis = PMlist_distance[solution[i]][solution[j]]
            vm_dis_sum += vm_dis
            dis_count += 1
            if vm_dis == 1:
                edge_sum += VM_flow_matrix[i][j]
            elif vm_dis == 3:
                agge_sum += VM_flow_matrix[i][j]
            elif vm_dis == 5:
                core_sum += VM_flow_matrix[i][j]
                
''' Average Hops per Flow ''' 
average_hop = vm_dis_sum / dis_count                 
info = "  3. Average Hops per Flow: " + str(average_hop) + "\n"
print info 
write_str_to_file(info, resultLoc)

''' Core/Aggregate/Edge ''' 
info = "  2. Core: " + str(core_sum) + " /Aggregate: " + \
                  str(agge_sum+edge_sum) + " /Edge:" + str(edge_sum+agge_sum+core_sum) + "\n"
print info
write_str_to_file(info, resultLoc)

''' pm_sum '''
pms = set([])
for pm in solution:
    pms.add(pm)
info = '  3. pm_sum: ' + str(len(pms)) + "\n"
print info
write_str_to_file(info, resultLoc)






