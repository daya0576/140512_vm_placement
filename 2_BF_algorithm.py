'''
python + " 2_BF_algorithm.py " + fileLoc + pmType + " >> " + resultLoc

'''
import sys
import common_funs.comm_funs as comm
import time
local_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))

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

def init_PMlist():
	PMlist = []
	for i in xrange(1024):
		PMlist.append([])
	return PMlist	

def init_PMlist_capacity():
	PMlist_capicity = []
	for i in xrange(1024):
		PMlist_capicity.append([PM_capacity_cpu, PM_capacity_mem])
	return PMlist_capicity

def place_VM_in_PM(node, location):
	global PMlist, PMlist_capacity
	PMlist[location].append(node)
	PMlist_capacity[location][0] -= VMlist_cost[node][0]
	PMlist_capacity[location][1] -= VMlist_cost[node][1]

def compute_VM_to_PM(PMlist):
	VM_to_PM = [0] * 1024
	
	for PM in PMlist:
		for VM in PM:
			VM_to_PM[VM] = PMlist.index(PM)
	'''
	for i, vm in enumerate(VMlist):
		VM_to_PM[vm] = i
	'''
	
# 	print "VM_position", VM_to_PM
	comm.write_line_to_file(VM_to_PM, "1_MC_BT_result/tubo_solution.data")
	#print len(VM_to_PM)	
	return VM_to_PM

def Pod_best_fit(VMlist, VMlist_cost):
	print ''' Best Fit~~'''	
	place_VM_in_PM(VMlist[0], 0)
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
			place_VM_in_PM(VM, VM_best_location)

def Pod_first_fit(VMlist, VMlist_cost):
	print ''' First Fit~~'''	
	place_VM_in_PM(VMlist[0], 0)
	pm_flag = 0
	for VM in VMlist:
		if(VMlist.index(VM) >= 1):
			VM_cost_cpu = VMlist_cost[VM][0]
			VM_cost_mem = VMlist_cost[VM][1]
			
			PM_cpu_left = PMlist_capacity[pm_flag][0] - VM_cost_cpu
			PM_mem_left = PMlist_capacity[pm_flag][1] - VM_cost_mem
			if(PM_cpu_left >= 0 and PM_mem_left >= 0):
				place_VM_in_PM(VM, pm_flag)
			else:
				pm_flag += 1
				place_VM_in_PM(VM, pm_flag)


def show_pm_info(PMlist, VMlist_cost):
	final_cpu_result = [0]*1024
	final_mem_result = [0]*1024
	pm_count = 0
	for i, vms in enumerate(PMlist):
		for vm in vms:
			final_cpu_result[i] += VMlist_cost[vm][0]
			final_mem_result[i] += VMlist_cost[vm][1]
		if final_cpu_result[i] + final_mem_result[i] > 0:
			pm_count += 1
	
	final_cpu_result = [str(f1)[0:5] for f1 in final_cpu_result]
	final_mem_result = [str(f2)[0:5] for f2 in final_mem_result]
# 	final_cpu_result = [float(s1) for s1 in final_cpu_result]
# 	final_mem_result = [float(s2) for s2 in final_mem_result]

	print "final_cpu_result: " + str(final_cpu_result)
	input = "test/exp/final_cpu_result"
	output = "test/exp/final_cpu_result.xls"
	comm.write_line_to_file(final_cpu_result, input)
	comm.list2xls(input, output)
	
	print "final_mem_result: " + str(final_mem_result)
	input = "test/exp/final_mem_result"
	output = "test/exp/final_mem_result.xls"
	comm.write_line_to_file(final_mem_result, input)
	comm.list2xls(input, output)
	
	print "pm_sum: " + str(pm_count) + "/1024"


'''
Algorithms2 BF-HC algorithm
'''		
print "-------------Algorithms2 BF-HC algorithm---------------"
''' init PM '''
PM_capacity_cpu = 1.0
PM_capacity_mem = 1.0
PM_cpu_weight = 1.0
PM_capacity = PM_capacity_cpu * PM_cpu_weight + PM_capacity_mem

vm_flow_file = sys.argv[1]
vm_flow_file_loc = "input/vm_flow_matrix/" + vm_flow_file + ".data"
print vm_flow_file_loc
dir_name = "test/" + local_date
resultLoc = sys.argv[4]
#"input/vm_flow_matrix/4Partitions@5percent.data"
nodes_result = read_line_from_file("1_MC_BT_result/nodes_result.data")
pm_dist_file = "input/pm_distance/pm_distanc_1024.data"
#vm_cpu_mem_file = "input/vm_cost/Node1024_cpu0.5_men0.3_stdvar0.5"
vm_cpu_mem_file = sys.argv[2]
fit_method = sys.argv[3]

VMlist = nodes_result
#VMlist = range(1024)
print "len(nodes_result):", len(nodes_result)


VMlist_cost = read_cpu_mem_from_file(vm_cpu_mem_file)
PMlist_distance = read_matrix(pm_dist_file)
VM_flow_matrix = read_matrix(vm_flow_file_loc)


''' Fit~~'''	
PMlist = init_PMlist()
PMlist_capacity = init_PMlist_capacity()

if fit_method == "best":
	Pod_best_fit(VMlist, VMlist_cost)
elif fit_method == "first":
	Pod_first_fit(VMlist, VMlist_cost)

show_pm_info(PMlist, VMlist_cost)

VM_to_PM = compute_VM_to_PM(PMlist)
print VM_to_PM
comm.write_line_to_file(VM_to_PM, "test/mapping_result/solution.data")


