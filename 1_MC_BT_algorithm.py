import networkx as nx
try:
	import matplotlib.pyplot as plt
except:
	raise
import random
import sys

result_G = []
vm_flow_file = sys.argv[1]
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

def write_lines_to_file(result_G_nodes, filename):
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

def draw_graph(G_origin):
	elarge=[(u,v) for (u,v,d) in G_origin.edges(data=True) if d['weight'] >0.5]
	esmall=[(u,v) for (u,v,d) in G_origin.edges(data=True) if d['weight'] <=0.5]
	
	pos=nx.spring_layout(G_origin) # positions for all nodes
	
	# nodes
	nx.draw_networkx_nodes(G_origin,pos,node_size=300)
	
	# edges
	nx.draw_networkx_edges(G_origin,pos,edgelist=elarge,
	                    width=3)
	nx.draw_networkx_edges(G_origin,pos,edgelist=esmall,
	                    width=3,alpha=0.5,edge_color='b',style='dashed')
	
	# labels
	nx.draw_networkx_labels(G_origin, pos, font_size=10, font_family='sans-serif')
	
	plt.axis('off')
	plt.savefig("weighted_graph.png") # save as png
	plt.show() # display



#Initial G = (V, E)

G_origin = nx.Graph() 

file_lists = read_lines_from_file(vm_flow_file)

G_origin_lists = file_lists_to_G_lists(file_lists)
print "total_nodes:", total_nodes
print "total_edges:", total_edges

G_origin.add_weighted_edges_from(G_origin_lists)
vm_active_list = G_origin.nodes()
wcc = nx.connected_component_subgraphs(G_origin)

result_G_nodes = []
for sub_G in wcc:
	print sub_G.nodes()
	for node in sub_G.nodes():
		result_G_nodes.append(node)


print "result_G_nodes", result_G_nodes
print "len", len(result_G_nodes)
write_lines_to_file(vm_active_list, "1_MC_BT_result/nodes_result.data")


#draw_graph(G_origin)

