import sys

def read_line_from_file(filename):
	file_object = open(filename)
	try:
		list_of_all_the_lines = file_object.readlines()
	finally:
		file_object.close()
	
	line_new = []
	line = list_of_all_the_lines[0].strip('\n').split(' ')
	for num in line:
		try:
			num = int(num)
			line_new.append(num)
		except ValueError:
			pass
	
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

def read_lines_from_file(filename):
	file_object = open(filename)
	try:
		lines = file_object.readlines()
	finally:
		file_object.close()
	
	return lines

def read_matrix(filename):
	return lines_to_list(read_lines_from_file(filename))

def read_cpu_mem_from_file(filename):
	lines = read_lines_from_file(filename)
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

def init_PMlist():
	PMlist = []
	for i in range(nodes_sum):
		PMlist.append([])
	return PMlist	

def init_PMlist_capacity():
	PMlist_capicity = []
	for i in range(nodes_sum):
		PMlist_capicity.append([PM_capacity_cpu, PM_capacity_mem])
	return PMlist_capicity

def place_VM_in_PM(node, location):
	global PMlist, PMlist_capacity
	PMlist[location].append(node)
	PMlist_capacity[location][0] -= VMlist_cost[node][0]
	PMlist_capacity[location][1] -= VMlist_cost[node][1]

def init_VM_position():
	VM_position = []
	for i in range(pm_sum):
		VM_position.append(-1)
	return VM_position
	
'''
Algorithms2 BF-HC algorithm
'''		
print "-------------algorithm2---------------"
vm_flow_file = sys.argv[1]
#"input/vm_flow_matrix/4Partitions@5percent.data"
nodes_result = read_line_from_file("1_MC_BT_result/nodes_result.data")
print nodes_result
nodes_sum = len(nodes_result)
print "nodes_sum", nodes_sum
pm_dist_file = "input/pm_distance/pm_distanc_1024.data"
vm_cpu_mem_file = "input/vm_cost/Node1024_cpu0.5_men0.3_stdvar0.5"

PM_capacity_cpu = 1
PM_capacity_mem = 1
PM_cpu_weight = 5.0
PM_capacity = PM_capacity_cpu * PM_cpu_weight + PM_capacity_mem

VMlist = nodes_result
PMlist = init_PMlist()
VMlist_cost = read_cpu_mem_from_file(vm_cpu_mem_file)
PMlist_capacity = init_PMlist_capacity()
#print "node 0 to node ",nodes_sum-1 ,"[cpu, mem]:", VMlist_cost

''' Best Fit~~'''	
place_VM_in_PM(VMlist[0], 0)
for VM in VMlist:
	#print VM, VMlist_cost[VM]
	#print PMlist_capacity
	if(VMlist.index(VM) >= 1):
		VM_cost_cpu = VMlist_cost[VM][0]
		VM_cost_mem = VMlist_cost[VM][1]
		PM_best_capacity_left = PM_capacity
		VM_best_locate = 0

		for PM in PMlist:
			PM_cpu_left = PMlist_capacity[PMlist.index(PM)][0] - VM_cost_cpu
			PM_mem_left = PMlist_capacity[PMlist.index(PM)][1] - VM_cost_mem
			PM_sum_left = PM_cpu_left * PM_cpu_weight + PM_mem_left
			if(PM_cpu_left >= 0 and PM_mem_left >= 0 
			      and PM_sum_left < PM_best_capacity_left):
				PM_best_capacity_left = PM_sum_left
				VM_best_location = PMlist.index(PM)
		place_VM_in_PM(VM, VM_best_location)
	
print PMlist


'''compute (distace * flow)'''
PMlist_distance = read_matrix(pm_dist_file)
VM_flow_matrix = read_matrix(vm_flow_file)

pm_sum = len(PMlist_distance)

VM_to_PM = init_VM_position()

for PM in PMlist:
	for VM in PM:
		VM_to_PM[VM] = PMlist.index(PM)

print "VM_position", VM_to_PM

final_result = 0
flow_sum = 0			
for VM1 in range(1024):
	for VM2 in range(1024):
		flow = VM_flow_matrix[VM1][VM2]
		distance = PMlist_distance[VM_to_PM[VM1]][VM_to_PM[VM2]]
		if flow > 0 and distance > 0:
			flow_sum += 1 
			#print final_result, ' += ', distance, ' * ',  flow
			final_result += distance * flow
	
final_result /= 2
print "sum(distace * flow):", final_result
print "flow_sum", flow_sum/2






































