import networkx as nx
import numpy as np
try:
    import matplotlib.pyplot as plt
except:
    raise

result_G = []
#vm_flow_file = sys.argv[1]
#vm_flow_file = "input/vm_flow_matrix/Inc_5Partition.data"
percentage = 5
filename = "2Partitions@" + str(percentage) + "percent"
vm_flow_file = "input/vm_flow_matrix/" + filename + ".data"
#vm_flow_file = "origin_generate/data/" + filename + ".data"
print vm_flow_file

total_edges = 0
total_nodes = 0

print "-------------pre processing---------------"
def lines_to_list(list_of_all_the_lines):
    list_new = []
    for line in list_of_all_the_lines:
        line = line.strip('\n')
        line = line.strip('\t')
        line = line.split()
        list_new.append(line)

    return list_new

def read_lines_from_file(filename):
    with open(filename, 'r') as f:  
        list_of_all_the_lines = f.readlines()
            
    return lines_to_list(list_of_all_the_lines)

def WriteMatrixIntoFile(matrix,fileName):
    with open(fileName, mode = "w") as fout:
        for row in matrix:
            for ele in row:
                fout.write(str(ele)+"\t")
            fout.write("\n")

def write_line_to_file(result_G_nodes, filename):
    with open(filename, 'w') as f:
        for result in result_G_nodes:
            result = str(result) + " "
            f.write(result)

def file_lists_to_G_lists(file_lists):
    global total_edges, total_nodes
    #total_nodes = len(file_lists)
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

def geneateNewMatrix(G_origin_lists, result_nodes):
    N = 1024
    G_result_matrix = np.zeros((N,N))
    for edge in G_origin_lists:
        if (edge[0] and edge[1]) in result_nodes:
            G_result_matrix[edge[0], edge[1]] = edge[2]    
            G_result_matrix[edge[1], edge[0]] = edge[2]     
    return G_result_matrix

def pre_test():
    global total_nodes
    #Initial G = (V, E)
    G_origin = nx.Graph()
    file_lists = read_lines_from_file(vm_flow_file)  
    G_origin_lists = file_lists_to_G_lists(file_lists)
    #print G_origin_lists
    G_origin.add_weighted_edges_from(G_origin_lists)
    draw_graph(G_origin)
    print G_origin.nodes()
    
    wcc = nx.connected_component_subgraphs(G_origin)
    
    G_sub_nodes = []
    G_result = []
    for G_sub in wcc:
        G_result.append(G_sub)
        G_sub_nodes.append(len(G_sub.nodes())) 
        total_nodes += len(G_sub.nodes())
        
    print "total_nodes:", total_nodes
    print "total_edges:", total_edges   
     
    print G_sub_nodes
    #draw_graph(G_origin)
    #draw_graph(G_result[0])
    
    #G_result_matrix = geneateNewMatrix(G_origin_lists, G_result[0].nodes())    
    #WriteMatrixIntoFile(G_result_matrix, "input/vm_flow_matrix/" + filename + "_treated.data");
    
    

if __name__ == '__main__':
    pre_test()

    
    
    
    
    
    
    