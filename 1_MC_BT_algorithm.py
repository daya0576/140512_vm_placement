import networkx as nx
from igraph import Graph
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

def gomory_hu_tree(graph, capacity=None, flow_attr="flow", copy_attrs=True):
    """Calculates the Gomory-Hu tree of the given graph, assuming that the edge
    capacities are given in `capacity`.

    This implementation uses Gusfield's algorithm.

    @param capacity: the vector of edge capacities. May be a list or the name
      of an edge attribute.
    @param flow_attr: the name of the edge attribute in the resulting graph that
      will contain the minimum flow values
    @param copy_attrs: whether to copy the graph and vertex attributes of the
      original graph into the returned one
    @return: the Gomory-Hu tree
    """
    n = graph.vcount()

    # Initialize the tree: every edge points to node 0
    neighbors = [0] * n
    flows = [0.0] * n

    # For each source vertex except vertex zero...
    for s in xrange(1, n):
        # Find its neighbor.
        t = neighbors[s]

        # Find the minimum cut between s and t
        cut = graph.mincut(s, t, capacity)
        flows[s] = cut.value
        side_of_s = cut[cut.membership[s]]

        # Update the tree
        for u in side_of_s:
            if u > s and neighbors[u] == t:
                neighbors[u] = s

    # Construct the tree
    edges = [(i, neighbors[i]) for i in xrange(1, n)]
    result = Graph(n, edges, directed=False, edge_attrs={flow_attr: flows[1:]})
    
    # Copy the attributes if needed
    if copy_attrs:
        for attr in graph.attributes():
            result[attr] = graph[attr]
        for attr in graph.vertex_attributes():
            result.vs[attr] = graph.vs[attr]

    return result

def xg_to_ig(xg):
	weights = []

	for edge in xg.edges():
		weights.append(G_origin[edge[0]][edge[1]]['weight'])

	ig = Graph(xg.edges())
	ig.es["capacity"] = weights

	return ig

def ig_to_xg():
	pass
#Initial G = (V, E)

G_origin = nx.Graph()

file_lists = read_lines_from_file(vm_flow_file)

G_origin_lists = file_lists_to_G_lists(file_lists)
print "total_nodes:", total_nodes
print "total_edges:", total_edges

G_origin.add_weighted_edges_from(G_origin_lists)

vm_active_list = G_origin.nodes()
wcc = nx.connected_component_subgraphs(G_origin)

for sub_G in wcc:
	print sub_G.nodes()
	print sub_G.edges()
	print 
	
	ig = xg_to_ig(sub_G)
	for edge in ig.es:
		print edge.tuple, edge['capacity']
	print 
	
	gh = ig.gomory_hu_tree()
	for edge in gh.es:
		print edge.tuple, edge['flow']
	print 
	
	exit()


