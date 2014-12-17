# -*- coding: utf-8 -*- 

class Node:
    """
    Tree node: left and right child + data which can be any object
    """
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data
        self.parent = "1"

    def insert_both(self, node_left, node_right):
        if self.children_count() == 0:
            if self.parent == self.data.order:
                self.left = node_left
                #print len(node_left.data.vms)
                self.right = node_right
                #print len(node_right.data.vms)
                #print "insert success"
                return

        if self.left:
                self.left.insert_both(node_left, node_right)
        if self.right:
                self.right.insert_both(node_left, node_right)
    
    def find_parent(self, child0):  
        #print root
        #print "search node", root.data.order
        if self.left:
            self.left.find_parent(child0)  
        if self.right:
            self.right.find_parent(child0) 
            
        if self.children_count() == 0:
            if child0 in self.data.vms:
                #print "find parent:", self.data.order, self.data.vms
                self.parent = self.data.order  
          
    def children_count(self):
        """
        Returns the number of children

        @returns number of children: 0, 1, 2
        """
        cnt = 0
        if self.left:
            cnt += 1
        if self.right:
            cnt += 1
        return cnt

    def print_tree(self):
        """
        Print tree content inorder
        """
        if self.left:
            self.left.print_tree()
        print (self.data.order, 
               len(self.data.vms), 
               #self.data.cpu_sum, 
               #self.data.mem_sum 
               #self.data.flow_sum,
               #self.data.intra_flow
               ),
               
        if self.right:
            self.right.print_tree()
    
    def midTraverse(self):
        if self.left:
            self.left.midTraverse()
            
        if self.children_count() == 0:
            print (self.data.order, self.data.vms),
            
        if self.right:
            self.right.midTraverse()
                
    def compute_intra_flow(self):
        if self.left and self.right:
            self.data.intra_flow = self.data.flow_sum[0] - (self.left.data.flow_sum[0]+self.right.data.flow_sum[0])
            
        if self.left:
            self.left.compute_intra_flow()
        if self.right:
            self.right.compute_intra_flow()
                
    def printbittree(self, n):
        if (self.right or self.left) is None:
            #print "  " * (n) + len(self.data.vms)
            self.print_node(n)
            return 
        
        if self.left:
            self.left.printbittree(n+1)
        #print "  " * (n) + len(self.data.vms)
        self.print_node(n)
        if self.right:
            self.right.printbittree(n+1)
    
    def print_node(self, n):
        with open("btree/tree_result.data", mode = "a") as fout:
            fout.write("  " * 8*n + str(len(self.data.vms)) + "(" + 
                       str(len(self.data.order)) + ", " +  
                       str("%.1f"%self.data.intra_flow) + ", " + 
                       str("%.1f"%self.data.flow_sum[0]) + ", " + 
                       str("%.1f"%self.data.flow_sum[1]) + ", " + 
                       #str("%.2f"%self.data.cpu_sum) + ", " + 
                       #str("%.2f"%self.data.mem_sum) + ")" + 
                       ")\n")
                
    def delete(self, order):
        if self.left:
            self.left.delete(order)  
            
        if self.right:
            self.right.delete(order) 
        
        if order[0:-1] == self.data.order:
            #print "to delete order:", order
            #print "parent order:", self.data.order
            
            if len(order) == 1:
                print "don't destroy root..."
            else:
                if order[-1] == "2":
                    #print "delete left node " + order
                    self.left = None
                else:
                    #print "delete right node " + order
                    self.right = None
        
    def find_pod_nodes(self, layer, cpu_limit, mem_limit):
        if layer == len(self.data.order):
            if self.data.cpu_sum<cpu_limit and \
                self.data.mem_sum<mem_limit:
                return self
        
        node_left = None
        node_right = None
        if self.left:
            node_left = self.left.find_pod_nodes(layer, cpu_limit, mem_limit) 
            
        if self.right:
            node_right = self.right.find_pod_nodes(layer, cpu_limit, mem_limit) 
            
        if node_left != None: return node_left
        elif node_right != None: return node_right
        else: return None
        
    def get_depth(self):
        #分别求左右子树的深度，通过加1得到该树的深度，分而治之
        ldepth = 0
        rdepth = 0
        
        if self.left:
            ldepth = self.left.get_depth()
        
        if self.right:
            rdepth = self.right.get_depth()
            
        #关键之处，递归逻辑体(Math.max(ldepth,rdepth)替换之
        #!!!
        temp = 0;
        if (ldepth >= rdepth):
            temp = ldepth
        else:
            temp = rdepth
        return temp + 1;
    
    def get_ordered_vms(self):
        #分别求左右子树的深度，通过加1得到该树的深度，分而治之
        l_vms = []
        r_vms = []
        
        if self.left:
            l_vms = self.left.get_ordered_vms()
            
        if self.right:
            r_vms = self.right.get_ordered_vms()
            
        if self.children_count() == 0:
            if (self.data.order)[-1] == "1":
                l_vms.append((self.data.vms)[0])
            elif (self.data.order)[-1] == "2":
                r_vms.append((self.data.vms)[0])
            else:
                print "!!!"
                
        #return r_vms+l_vms
        return l_vms+r_vms

            

        

        
        
        
        
        
        
        
        