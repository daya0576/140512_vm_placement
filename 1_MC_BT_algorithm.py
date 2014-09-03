import networkx as nx
from igraph import Graph
try:
    import matplotlib.pyplot as plt
except:
    raise
import sys

result_G = []
vm_flow_file = sys.argv[1]
sort_method = sys.argv[2]

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

def sort_weight_by(G_x):
    vm_active_weight = {}
    for vm in G_x.nodes():
        weight = 0
        for edge in nx.all_neighbors(G_x, vm):
            weight += G_x[vm][edge]['weight']
        vm_active_weight[vm] = weight
    
    nodes_weight = sorted(vm_active_weight.iteritems(), key=lambda vm_active_weight:vm_active_weight[1], reverse=True)
    
    return nodes_weight

def sort_weight_by_both(G_hu, G_origin):
    vm_active_weight_hu = {}
    vm_active_weight_origin = {}
    for vm in G_hu.nodes():
        weight = 0
        for edge in nx.all_neighbors(G_hu, vm):
            weight += G_hu[vm][edge]['weight']
        vm_active_weight_hu[int(vm)] = weight
        weight = 0
        vm = int(vm)
        for edge in nx.all_neighbors(G_origin, vm):
            weight += G_origin[vm][edge]['weight']
        vm_active_weight_origin[vm] = weight
        
    
    #nodes_weight_hu = sorted(vm_active_weight_hu.iteritems(), key=lambda vm_active_weight_hu:vm_active_weight_hu[0], reverse=False)
    nodes_weight_origin = sorted(vm_active_weight_origin.iteritems(), key=lambda vm_active_weight_origin:vm_active_weight_origin[1], reverse=True)
    
    #print nodes_weight_hu
    
    nodes_weight = {}
    for node in nodes_weight_origin:
        if node[1] == 0:
            weight = 0
        else:
            #print node[0]
            weight = vm_active_weight_hu[node[0]] / node[1]
            #print vm_active_weight_hu[node[0]], node[1]
        nodes_weight[node[0]] = weight
    
    nodes = sorted(nodes_weight.iteritems(), key=lambda nodes_weight:nodes_weight[1], reverse=True)
    print nodes

    return nodes
          
def sort_weight_by_iter(G_hu):
    result_G_nodes = []
    while len(G_hu.nodes()) > 0:
        vm_active_weight = {}
        for vm in G_hu.nodes():
            weight = 0
            for node in nx.all_neighbors(G_hu, vm):
                weight += G_hu[vm][node]['weight']
            vm_active_weight[vm] = weight
        
        nodes_weight = sorted(vm_active_weight.iteritems(), key=lambda vm_active_weight:vm_active_weight[1], reverse=True)
        #print nodes_weight
        result_G_nodes.append(nodes_weight[0][0])
        G_hu.remove_node(nodes_weight[0][0])
    
    print "result_G_nodes", result_G_nodes
    return result_G_nodes

result_G = []
def sort_by_edge_and_tree(G_sub, std):
    global result_G
    '''test'''
    print "std", std
    #draw_graph(G_sub)
    
    edges = G_sub.edges()
    for edge in edges:
        edge_weight = G_sub[edge[0]][edge[1]]["weight"]
        if edge_weight <= std:
            #print edge, edge_weight
            G_sub.remove_edge(edge[0], edge[1])
    
    wcc = nx.connected_component_subgraphs(G_sub)
    
    G_index = result_G.index(G_sub)
    result_G.remove(G_sub)
    big_G_list = []
    for G_rep in wcc:
        result_G.insert(G_index, G_rep)
        G_index += 1
        
        if len(G_rep.nodes()) > 3:
            big_G_list.append(G_rep)
            
    print [G_show.nodes() for G_show in result_G]
    #print "len(result_G)", len(result_G)
    
    for G_big in big_G_list:
        sort_by_edge_and_tree(G_big, (std+0.03)*1.1)
    

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

    result_G_nodes = []
    #result_G_nodes = sort_weight_by_iter(G_hu)
    if "-a" in sort_method:
        result_G_nodes = G_origin.nodes()
        
    elif  "-n" in sort_method:
        print "sort_weight_by(G_origin)"
        nodes_weight = sort_weight_by(G_origin)
        result_G_nodes = [node[0] for node in nodes_weight]
        print "result_G_nodes", result_G_nodes
        
    elif "-h" in  sort_method:
        nodes_weight = sort_weight_by(G_hu)
        result_G_nodes = [node[0] for node in nodes_weight]
        print "result_G_nodes", result_G_nodes
        print "sort_weight_by(G_hu)"
        
    elif "-b" in  sort_method:
        nodes_weight = sort_weight_by_both(G_hu, G_origin)
        result_G_nodes = [node[0] for node in nodes_weight]
        print "result_G_nodes", result_G_nodes
        print "sort_weight_by_both(G_hu, G_origin)"
        
    elif "-z" in sort_method:
        global result_G
        '''print [[edge[0], edge[1], G_hu[edge[0]][edge[1]]["weight"]]for edge in G_hu.edges()]
        
        for edge in G_hu.edges():
            weight_G_hu = G_hu[edge[0]][edge[1]]["weight"]
            
            if int(edge[0]) < int(edge[1]):
                edge_origin = (int(edge[0]), int(edge[1]))
            else:
                edge_origin = (int(edge[1]), int(edge[0]))
            if edge_origin in G_origin.edges():
                weight_G_origin = G_origin[edge_origin[0]][edge_origin[1]]["weight"]
            else:
                weight_G_origin = 0
                
            if weight_G_origin == 0:
                G_hu[edge[0]][edge[1]]["weight"] = 0
            else:
                G_hu[edge[0]][edge[1]]["weight"] = weight_G_hu - weight_G_origin
            
        print [[edge[0], edge[1], G_hu[edge[0]][edge[1]]["weight"]]for edge in G_hu.edges()]
        '''
        #draw_graph(G_hu)
        result_G = [G_hu]
        sort_by_edge_and_tree(G_hu, 0)
        
        for G_sub in result_G:
            result_G_nodes += G_sub.nodes()
            
        print "result_G_nodes:", result_G_nodes
        print "len:", len(result_G_nodes)
        print "sort_by_tree(G_hu, G_origin)"
        
        
    write_lines_to_file(result_G_nodes, "1_MC_BT_result/nodes_result.data")

if __name__ == "__main__" :
    test_gomory_hu()


        
        


