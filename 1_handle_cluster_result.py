import sys
from btree.btree_test import Node
from btree.node_data import NodeData
import time
import common_funs.comm_funs as comm
#print time.time()

#print "-------------algorithm1---------------"
print "algorithm1".center(40, '-')

pm_dist_file = "input/pm_distance/pm_distanc_1024.data"

'''
N = 7
vm_flow_file = "input/vm_flow_matrix/test_daya1.data "
act_nodes_file = "1_MC_BT_result/nodes_activity.data"
#mat_result_file = "input/cluster_result/" + sys.argv[1] + "_1024.data"
mat_result_file = "input/cluster_result/test_daya1_ncut_1024.data"
vm_cpu_mem_file = "input/vm_cost/Node7"
'''
N = 1024
vm_flow_file = "origin_generate/data/2Partitions@13percent.data "
#mat_result_file = "input/cluster_result/" + sys.argv[1] + "_1024.data"
mat_result_file = "input/cluster_result/" + "2Partitions@13percent_ncut" + "_1024.data"
vm_cpu_mem_file = "input/vm_cost/Node1024_cpu0.2_men0.2_stdvar1"
print mat_result_file
print vm_cpu_mem_file


def write_lines_to_file(result_G_nodes, filename):
    with open(filename, 'w') as f:
        for result in result_G_nodes:
            result = str(result) + " "
            f.write(result)
 
def read_line_from_file(filename):
    with open(filename) as f:
        line_result = f.readlines()
    
    line = line_result[0].strip('\n').split(' ')
    line_new = [int(i) for i in line if len(i)>0]
    
    return line_new

def read_lines_from_file(filename):
    with open(filename) as f:
        list_of_all_the_lines = f.readlines()

    list_new = []
    for line in list_of_all_the_lines:
        line = line.split(',')
        line_int = [int(str1) for str1 in line]
        list_new.append(line_int)
        #print line_int 

    return list_new

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

def read_cpu_mem_from_file(filename):
    with open(filename) as file_object:
        lines = file_object.readlines()
    lines_new = []
    for line in lines:
        line.replace("\t", " ")
        line = line.split()
        line_new = []
        for num in line:
            num = float(num)
            line_new.append(num)
        
        lines_new.append(line_new)
    return lines_new
    
def compute_cost(VMlist_cost, vms):
    cpu_sum = 0
    mem_sum = 0
    for vm in vms:
        cpu_sum += VMlist_cost[vm][0]
        mem_sum += VMlist_cost[vm][1]
    
    return cpu_sum, mem_sum
 
def compute_sum_flow(VM_flow_matrix, vms):
    flow_sum_in = 0
    flow_sum_out = 0
    for vm1 in vms:
        for vm2, flow in enumerate(VM_flow_matrix[vm1]):
            if flow > 0:
                if vm2 in vms:
                    flow_sum_in += flow/2
                else:
                    flow_sum_out += flow
                    #print flow_sum_out
                
    return flow_sum_in, flow_sum_out
    
def generate_cluster():
    file_lists = read_lines_from_file(mat_result_file) 
    num_of_cuts = len(file_lists[0]);
    cluster_result = [];
    for i in range(num_of_cuts):
        cluster_result.append(
            [int(list1[i])for list1 in file_lists]);
    
    return cluster_result

def init_root(VMlist_cost, VM_flow_matrix):
    node_tmp = NodeData("1", range(N))  
    node_tmp.cpu_sum, node_tmp.mem_sum = compute_cost(VMlist_cost, range(N))
    node_tmp.flow_sum = compute_sum_flow(VM_flow_matrix, range(N))
    
    vms_root = Node(node_tmp) 
    
    return vms_root
 
def handle(cluster_result, vms_root, VMlist_cost, 
           VM_flow_matrix, activity_nodes):
    #print "cut".center(30, '-')
    cluster_result.insert(0, [1]*len(cluster_result[0]));
    binary_result = ["1"]*len(cluster_result)
    
    for k, single_result in enumerate(cluster_result):
        vms_left = []
        vms_right = []
        if k == 0:continue
        
        # step 1: right and left list
        cut_node = 0
        for (vm, single_node) in enumerate(single_result):
            pre_node = cluster_result[k-1][vm]
            if single_node != pre_node:
                cut_node = pre_node
                binary_result[vm] += "2"
                vms_left.append(vm)
                
        for (vm, single_node) in enumerate(single_result): 
            pre_node = cluster_result[k-1][vm]  
            #print pre_node, single_node, cut_node       
            if cut_node == pre_node and cut_node == single_node:
                binary_result[vm] += "1"
                vms_right.append(vm) 
                
        #print "vms_left:", vms_left, 
        #print "vms_right", vms_right      
        
        # step 2: find parent
        #vms_parent = vms_left + vms_right
        #print "vms_parent", vms_parent
        #print "parent", binary_result_left[0:-1]
        vms_root.find_parent(vms_left[0])
        
        #step 3: define data and insert
        #plus: filter nodes without flow
        if len(set(vms_left) & set(activity_nodes)) != 0:
        #if True:
            node_data_left = NodeData(binary_result[vms_left[0]], vms_left)  
            node_data_left.cpu_sum, node_data_left.mem_sum = compute_cost(VMlist_cost, vms_left)
            #flow_sum_in, flow_sum_out = compute_sum_flow(VM_flow_matrix, vms_left)
            node_data_left.flow_sum = compute_sum_flow(VM_flow_matrix, vms_left)
            node_left = Node(node_data_left) 
        else:
            node_left = None
            
        if len(set(vms_right) & set(activity_nodes)) != 0:
        #if True:
            node_data_right = NodeData(binary_result[vms_right[0]], vms_right)
            node_data_right.cpu_sum, node_data_right.mem_sum = compute_cost(VMlist_cost, vms_right)
            node_data_right.flow_sum = compute_sum_flow(VM_flow_matrix, vms_right)
            node_right = Node(node_data_right) 
        else:
            node_right = None
        
        vms_root.insert_both(node_left, node_right)
        
        #step 4: compute intra flow
        vms_root.compute_intra_flow()
        
    return binary_result, vms_root

def next_lower(a, b):
    length1 = len(a if len(a) < len(b) else b);
        
    for i in range(length1):
        if int(b[i]) < int(a[i]):
            return True
        elif int(b[i]) > int(a[i]):
            return False
   
def sort_nodes(binary_result, avtivity_nodes):
    vms =  range(len(binary_result))
    
    for i in range(len(vms)):
        for j in range(len(vms)-i-1):
            if next_lower(binary_result[j], binary_result[j+1]):
                vms[j], vms[j + 1] = vms[j + 1], vms[j]
                binary_result[j] , binary_result[j+1] = \
                binary_result[j+1] , binary_result[j]
    print binary_result
        #print vms
    return vms

def sort_nodes1(binary_result, vms):
    print vms
    act_binary_result = [binary_result[node] for node in vms]
    
    for i in range(len(vms)):
        for j in range(len(vms)-i-1):
            if next_lower(act_binary_result[j], act_binary_result[j+1]):
                vms[j], vms[j + 1] = vms[j + 1], vms[j]
                act_binary_result[j] , act_binary_result[j+1] = \
                act_binary_result[j+1] , act_binary_result[j]
    
    #print act_binary_result
    return vms

def find_hier_solution(vms_root, cpu_limit, mem_limit):
    hier_solution = []
    depth = vms_root.get_depth() + 1
    for layer in range(depth):
        if layer == 0: continue 
        if layer > vms_root.get_depth(): break
        #print "layer", layer
        
        pod_nodes = vms_root.find_pod_nodes(layer, cpu_limit, mem_limit)
        #print pod_nodes
        while pod_nodes:
            hier_solution.append(pod_nodes)
            vms_root.delete(pod_nodes.data.order)
            pod_nodes = vms_root.find_pod_nodes(layer, cpu_limit, mem_limit)
    
    return hier_solution
    
def print_hier_solution(hier_solution, activity_nodes):
    print len(activity_nodes)
    for pod_node in hier_solution:
        print pod_node.data.cpu_sum, pod_node.data.mem_sum
        print len(pod_node.data.vms)
        print pod_node.data.vms[0], pod_node.data.vms[3]
        tmp = True
        for vm in pod_node.data.vms:
            if vm not in activity_nodes:
                tmp = False
        print tmp

def init_PMlist(pm_num):
    PMlist = []
    for i in xrange(pm_num):
        PMlist.append([])
    return PMlist    

def init_PMlist_capacity(PM_capacity_cpu, PM_capacity_mem, pm_num):
    PMlist_capicity = []
    for i in xrange(pm_num):
        PMlist_capicity.append([PM_capacity_cpu, PM_capacity_mem])
    return PMlist_capicity

  
def Pod_best_fit(VMlist, VMlist_cost, pm_num):
    PM_capacity_cpu = 1.0
    PM_capacity_mem = 1.0
    PM_cpu_weight = 1.0
    PM_capacity = PM_capacity_cpu * PM_cpu_weight + PM_capacity_mem
    PMlist = init_PMlist(pm_num)
    PMlist_capacity = init_PMlist_capacity(PM_capacity_cpu, PM_capacity_mem, pm_num)
    #print PMlist
    
    ''' Best Fit~~'''    
    PMlist[0].append(VMlist[0])
    PMlist_capacity[0][0] -= VMlist_cost[VMlist[0]][0]
    PMlist_capacity[0][1] -= VMlist_cost[VMlist[0]][1]
    for VM in VMlist:
        #print VM, VMlist_cost[VM]
        #print PMlist_capacity
        if(VMlist.index(VM) >= 1):
            VM_cost_cpu = VMlist_cost[VM][0]
            VM_cost_mem = VMlist_cost[VM][1]
            PM_best_capacity_left = PM_capacity
            VM_best_location = 0
    
            for PM in PMlist:
                PM_cpu_left = PMlist_capacity[PMlist.index(PM)][0] - VM_cost_cpu
                PM_mem_left = PMlist_capacity[PMlist.index(PM)][1] - VM_cost_mem
                PM_sum_left = PM_cpu_left * PM_cpu_weight + PM_mem_left
                if(PM_cpu_left >= 0 and PM_mem_left >= 0
                      and PM_sum_left < PM_best_capacity_left):
                    PM_best_capacity_left = PM_sum_left
                    VM_best_location = PMlist.index(PM)
            #place_VM_in_PM(VM, VM_best_location)
            PMlist[VM_best_location].append(VM)
            PMlist_capacity[VM_best_location][0] -= VMlist_cost[VM][0]
            PMlist_capacity[VM_best_location][1] -= VMlist_cost[VM][1]
    
    return PMlist
     
def cal_VM_to_PM(hier_solution, VMlist_cost):
    VM_to_PM = [0] * 1024
    for pod_order, pod_node in enumerate(hier_solution):
        print ("Pod"+str(pod_order)).center(30, '-')
        print pod_node.data.order
        print "cpu_sum", str(("%.2f"%pod_node.data.cpu_sum))+"/64", 
        print "mem_sum", str(("%.2f"%pod_node.data.mem_sum))+"/64"
        print "(flow_sum_in, flow_sum_out)", pod_node.data.flow_sum
        ordered_vms = pod_node.get_ordered_vms()
        print "vm sum:", len(ordered_vms)
        #Pod_list =  Pod_best_fit(ordered_vms, VMlist_cost)
        Pod_list =  Pod_best_fit(pod_node.data.vms, VMlist_cost, 100)
        
        #compute rest pm
        #print Pod_list
        pm_rest = 0
        for pm in Pod_list:
            if len(pm) is 0:
                pm_rest += 1
        print "pm_used", 100-pm_rest
        
        for pm_order, pm in enumerate(Pod_list):
            for vm in pm:   
                VM_to_PM[vm] = pm_order + 64 * pod_order
                
    return VM_to_PM

def cal_VM_to_PM_origin( VMlist_cost, vms_root):    
    VM_to_PM = [0] * 1024
    vms = []
    '''
    for pod_order, pod_node in enumerate(hier_solution):
        print pod_node.data.cpu_sum, pod_node.data.mem_sum
        vms += pod_node.get_ordered_vms()
    '''
    vms = vms_root.get_ordered_vms()
    #print vms
    #print len(vms)  
    
      
    Pod_list =  Pod_best_fit(vms, VMlist_cost, 1024)
    for pm_order, pm in enumerate(Pod_list):
        for vm in pm:   
            VM_to_PM[vm] = pm_order
            #print VM_to_PM[vm]
    
    return VM_to_PM

def cal_final_result(VM_flow_matrix, PMlist_distance, VM_to_PM):
    final_result = 0
    flow_sum = 0            
    for VM1 in xrange(1024):
        for VM2 in xrange(VM1):
            flow = VM_flow_matrix[VM1][VM2]
            distance = PMlist_distance[VM_to_PM[VM1]][VM_to_PM[VM2]]
            if flow > 0 and distance > 0:
                flow_sum += 1 
                #print final_result, ' += ', distance, ' * ',  flow
                final_result += distance * flow
    return final_result

def test_matlab_result():
    print "sort_by_cluster(matlab)"
    VM_flow_matrix = read_matrix(vm_flow_file)
    PMlist_distance = read_matrix(pm_dist_file)
    activity_nodes = comm.get_activity_nodes(vm_flow_file) 
    print "G_origin node sum:", len(activity_nodes)
    cluster_result = generate_cluster()
    VMlist_cost = read_cpu_mem_from_file(vm_cpu_mem_file)
    
    vms_root = init_root(VMlist_cost, VM_flow_matrix)
    
    print "generate binary_results..."   
    binary_result, vms_root = handle(cluster_result, vms_root, VMlist_cost, VM_flow_matrix, activity_nodes)
    #vms_root.delete("1")
    print "print tree(all nodes):",
    #vms_root.print_tree()
    print "\nprint tree(midTraverse):",
    #vms_root.midTraverse()
    vms_root.printbittree(0)
    
    print "\ndepth", vms_root.get_depth()
    
    # origin
    VM_to_PM = cal_VM_to_PM_origin(VMlist_cost, vms_root)
    #print VM_to_PM
    final_result = cal_final_result(VM_flow_matrix, PMlist_distance, VM_to_PM)    
    print "sum(distace * flow)_(origin):", final_result
    print 
    
    #hierarchy
    cpu_limit = 64*0.95
    mem_limit = 64*0.95
    hier_solution = find_hier_solution(vms_root, cpu_limit, mem_limit)
    #print_hier_solution(hier_solution, activity_nodes)
    #vms_root.printbittree(0)
    VM_to_PM = cal_VM_to_PM(hier_solution, VMlist_cost)
    #print "VM_to_PM:", VM_to_PM
    final_result = cal_final_result(VM_flow_matrix, PMlist_distance, VM_to_PM)    
    print "sum(distace * flow):", final_result


    
if __name__ == "__main__" :
    test_matlab_result()
    
    

    
    
    