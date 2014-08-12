import networkx as nx
from igraph import Graph
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


def xg_to_ig(xg):
    print "-----------xg_to_ig------------"
    ig = Graph()
    
    weights = [float(xg[edge[0]][edge[1]]['weight']) for edge in xg.edges()]
    for node in xg.nodes():
        ig.add_vertex(str(node))
    #print ig.vs["name"]

    edges = [(str(edge[0]), str(edge[1])) for edge in xg.edges()]
    ig.add_edges(edges)

    ig.es["capacity"] = weights
    

    return ig

def gh_to_xg(gh):
    print "--------------gh_to_xg---------------"
    nodes = gh.vs["name"]
    G_origin = nx.Graph()
    G_origin_lists = []
    for edge in gh.es:
        G_origin_lists.append([nodes[edge.tuple[0]], nodes[edge.tuple[1]], edge['flow']])
    
    #print G_origin_lists

    G_origin.add_weighted_edges_from(G_origin_lists)
    
    return G_origin

def domory_hu_tree_daya(G_origin):
    ig = xg_to_ig(G_origin)
    
    print "-----------generate gomory_hu_tree-------------"
    gh = ig.gomory_hu_tree(capacity= "capacity" , flow="flow"  )
    
    gh_x = gh_to_xg(gh)
    return gh_x

def sort_weight_by_desperate(G_hu):
    vm_active_weight = {}
    for vm in G_hu.nodes():
        weight = 0
        for edge in nx.all_neighbors(G_hu, vm):
            weight += G_hu[vm][edge]['weight']
        vm_active_weight[vm] = weight
    
    nodes_weight = sorted(vm_active_weight.iteritems(), key=lambda vm_active_weight:vm_active_weight[1], reverse=True)
    result_G_nodes = [node[0] for node in nodes_weight]
    
    print "result_G_nodes", result_G_nodes
    return result_G_nodes

def sort_weight_by(G_hu):
    result_G_nodes = []
    while len(G_hu.nodes()) > 0:
        vm_active_weight = {}
        for vm in G_hu.nodes():
            weight = 0
            for edge in nx.all_neighbors(G_hu, vm):
                weight += G_hu[vm][edge]['weight']
            vm_active_weight[vm] = weight
        
        nodes_weight = sorted(vm_active_weight.iteritems(), key=lambda vm_active_weight:vm_active_weight[1], reverse=True)
        #print nodes_weight
        result_G_nodes.append(nodes_weight[0][0])
        G_hu.remove_node(nodes_weight[0][0])
    
    print "result_G_nodes", result_G_nodes
    return result_G_nodes

def test_gomory_hu():
    #Initial G = (V, E)
    G_origin = nx.Graph()
    file_lists = read_lines_from_file(vm_flow_file)    
    G_origin_lists = file_lists_to_G_lists(file_lists)
    print "total_nodes:", total_nodes
    print "total_edges:", total_edges    
    G_origin.add_weighted_edges_from(G_origin_lists)
    #wcc = nx.connected_component_subgraphs(G_origin)

    G_hu = domory_hu_tree_daya(G_origin)
    result_G_nodes = sort_weight_by_desperate(G_hu)
    #result_G_nodes = sort_weight_by(G_hu)
    write_lines_to_file(result_G_nodes, "1_MC_BT_result/nodes_result.data")

if __name__ == "__main__" :
    test_gomory_hu()


        
        


