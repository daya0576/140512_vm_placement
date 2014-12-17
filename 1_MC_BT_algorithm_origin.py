import networkx as nx
import random
import sys

result_G = []
#vm_flow_file = sys.argv[1]
vm_flow_file = "input/vm_flow_matrix/5Partitions@25percent.data"
#"input/vm_flow_matrix/4Partitions@5percent.data"
sort = 0
total_edges = 0
total_nodes = 0


print "-------------algorithm1---------------"
def lines_to_list(list_of_all_the_lines):
	list_new = []
	for line in list_of_all_the_lines:
		line = line.strip('\n')
		line = line.strip('\t')
		line = line.split()
		list_new.append(line)

	return list_new

def read_lines_from_file(filename):
	file_object = open(filename)
	try:
		list_of_all_the_lines = file_object.readlines()
	finally:
		file_object.close()
			
	return lines_to_list(list_of_all_the_lines)

def write_lines_to_file(filename):
	file_object = open(filename, 'w')
	try:
		for result in result_G_nodes:
			result = str(result) + " "
			file_object.write(result)
		#simplejson.dump(result_G_nodes, file_object)
	finally:
		file_object.close()

def file_lists_to_G_lists(file_lists):
	global total_edges, total_nodes
	total_nodes = len(file_lists)
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
				total_edges += 1		
					
	return lines_new

def vm_sum(VMlist_flow_list):
	vm_all = []
	for vm_list in VMlist_flow_list:
		if vm_list[0] not in vm_all:
			vm_all.append(vm_list[0])
		if vm_list[1] not in vm_all:
			vm_all.append(vm_list[1])        
	return len(vm_all)

def G_to_nodes(list_G):
	nodes = []
	for G in list_G:
		nodes += G.nodes()
	return nodes

def G_to_edges_and_weights(list_G):
	G_weights = []
	for G in list_G:
		if(sum(edges_to_weights(G)) > 0):
			result_tmp = []
			result_tmp.append(G.edges()[0][0])
			result_tmp.append(G.edges()[0][1])
			result_tmp.append(sum(edges_to_weights(G)))
			G_weights.append(result_tmp)
	return G_weights

def G_to_weights(list_G):
	G_weights = []
	for G in list_G:
		if(sum(edges_to_weights(G)) >= 0):
			G_weights.append(sum(edges_to_weights(G)))
	return G_weights

def edges_to_weights(G):
	edges = G.edges()
	edges_weight = []
	i = 0
	for i in range(len(edges)):
		edges_weight.append(G[edges[i][0]][edges[i][1]]['weight'])
		
	return edges_weight

#While G has more than one node do mincut 

def mincut_Graph(G, node):
	global result_G
	if(G.number_of_nodes() >= 2):
					
		nodes_tmp = G.nodes()
		souce_node = random.choice(nodes_tmp)
		nodes_tmp.remove(souce_node)
		sink_node = random.choice(nodes_tmp)
		mincut_edges = nx.minimum_st_edge_cut(G, souce_node, sink_node, capacity='weight')		
		#print "cutted edges:", mincut_edges
		
		G.remove_edges_from(mincut_edges)

		wcc = nx.connected_component_subgraphs(G)
		if souce_node in wcc[0].nodes():
			G1 = wcc[0]
			G2 = wcc[1]
		else:
			G1 = wcc[1]
			G2 = wcc[0]
		
		G1_weights = edges_to_weights(G1)
		G1_weights_sum = sum(G1_weights)

		G2_weights = edges_to_weights(G2)
		G2_weights_sum = sum(G2_weights)
				
		if(G1_weights_sum > G2_weights_sum):
			result_G.insert(result_G.index(G), G1)
			result_G.insert(result_G.index(G) + 1, G2)
		else:
			result_G.insert(result_G.index(G) + 1, G1)
			result_G.insert(result_G.index(G), G2)
		
		result_G.remove(G)	
		
		mincut_Graph(G1, souce_node)
		mincut_Graph(G2, sink_node)
		
	else:
		return
		

#Initial G = (V, E)
G_origin = nx.Graph() 

file_lists = read_lines_from_file(vm_flow_file)

G_origin_lists = file_lists_to_G_lists(file_lists)
print "total_nodes:", total_nodes
print "total_edges:", total_edges

G_origin.add_weighted_edges_from(G_origin_lists)
wcc = nx.connected_component_subgraphs(G_origin)

vm_active_list = G_origin.nodes()
vm_active_list.sort()
#print "G:", vm_active_list
print "vm_sum:", len(G_origin.nodes())
'''
if sort == 1:
	for i in range(len(wcc)):
		for j in range(len(wcc)):
			if i < j:
				#if sum(edges_to_weights(wcc[i])) < sum(edges_to_weights(wcc[j])):
				if len(wcc[i].edges()) < len(wcc[j].edges()):
					tmp = wcc[i]
					wcc[i] = wcc[j]
					wcc[j] = tmp
'''

result_G.append(G_origin)
mincut_Graph(G_origin, 0)
result_G_nodes = G_to_nodes(result_G)	


print "final_result:", result_G_nodes
print "final_result_sum:", len(result_G_nodes)

write_lines_to_file("1_MC_BT_result/nodes_result.data")


			























