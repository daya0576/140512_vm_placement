'''
Created on 2014-5-12
'''
from operator import itemgetter, attrgetter 

def read_lines_from_file(filename):
    file_object = open(filename)
    try:
        list_of_all_the_lines = file_object.readlines()
    finally:
        file_object.close()   
    
    return list_of_all_the_lines

def lines_to_list(list_of_all_the_lines):
    list_new = []
    for line in list_of_all_the_lines:
        line_new = []
        line = line.strip('\n')
        line = line.strip('\t')
        line = line.split()
        for num in line:
            num = float(num)
            line_new.append(num)
        list_new.append(line_new)
    
    return list_new

def read_matrix_file(filename):
    return lines_to_list(read_lines_from_file(filename))
    
def tran_matrix(matrix):
    list_new = []
    for index_line, line in enumerate(matrix):
        for index_item, item in enumerate(line):
            if item != 0 and index_line < index_item:
            #if index_line < index_item:
                list_new.append([index_line, index_item, item])
    return list_new    

def vm_sum():
    vm_all = []
    for vm_list in VMlist_flow_list:
        if vm_list[0] not in vm_all:
            vm_all.append(vm_list[0])
        if vm_list[1] not in vm_all:
            vm_all.append(vm_list[1])        
    return len(vm_all)

def place_vm_one(vm_placed, vm): 
    global PMlist_dist_list
    pm_placed = VM_to_PM[vm_placed]
    i = 0
    placed = False
    while not placed:
        PM_pair = PMlist_dist_list[i]
        PM_placed = VM_to_PM.values()
        if PM_pair[0] == pm_placed and PM_pair[1] not in PM_placed:
            VM_to_PM[vm] = PM_pair[1]
            placed = True
            PMlist_dist_list.pop(i)
        elif PM_pair[1] == pm_placed and PM_pair[0] not in PM_placed:
            VM_to_PM[vm] = PM_pair[1]
            placed = True
            PMlist_dist_list.pop(i)
        i = i + 1
        
def place_vm_pair(vm1, vm2):
    i = 0
    placed = False
    while not placed:
        pm1 = PMlist_dist_list[i][0]
        pm2 = PMlist_dist_list[i][1]
        PM_placed = VM_to_PM.values()
        if pm1 not in PM_placed and pm2 not in PM_placed:
            VM_to_PM[vm1] = PMlist_dist_list[i][0]
            VM_to_PM[vm2] = PMlist_dist_list[i][1]
            placed = True
            PMlist_dist_list.pop(i)
        i = i + 1    
               
def place_vm(vm1, vm2, VM_to_PM):
    global PMlist_dist_list
    if VM_to_PM.has_key(vm1) and VM_to_PM.has_key(vm2):
        pass
    elif VM_to_PM.has_key(vm1):    
        place_vm_one(vm1, vm2)
    elif VM_to_PM.has_key(vm2):
        place_vm_one(vm2, vm1)
    else:
        place_vm_pair(vm1, vm2)

    return VM_to_PM
    
''' define '''
file_chiose = 1024

if file_chiose == 1:
    PMlist_dist_matrix = read_matrix_file("pm_and_vm_data/PMlist_dist.data")
    VMlist_flow_matrix = read_matrix_file("pm_and_vm_data/VMlist_flow.data")
elif file_chiose == 1024:
    PMlist_dist_matrix = read_matrix_file("input/pm_distance/pm_distanc_1024.data")
    VMlist_flow_matrix = read_matrix_file("input/vm_flow_matrix/1.data")
    
PMlist_dist_list = tran_matrix(PMlist_dist_matrix)
VMlist_flow_list = tran_matrix(VMlist_flow_matrix)

VM_sum = len(VMlist_flow_matrix)
PM_sum = len(PMlist_dist_matrix)

vm_all = []
for vm_list in VMlist_flow_list:
    if vm_list[0] not in vm_all:
        vm_all.append(vm_list[0])
    if vm_list[1] not in vm_all:
        vm_all.append(vm_list[1])

VM_to_PM = {}

''' sort '''
PMlist_dist_list.sort(key=itemgetter(2), reverse=False)
VMlist_flow_list.sort(key=itemgetter(2), reverse=True)
 
while len(VMlist_flow_list) > 0:
    vm1 = VMlist_flow_list[0][0]
    vm2 = VMlist_flow_list[0][1]

    VM_to_PM = place_vm(vm1, vm2, VM_to_PM)
    
    #print VM_to_PM
    VMlist_flow_list.pop(0)
    
print "result", VM_to_PM  
print "result_len", len(VM_to_PM)    
















