class NodeData:
    """
    Tree node data: oder + sum of cpu/mem sum flow + intra flow
    """
    def __init__(self, order, vms=None, VMlist_cost=None):
        """
        Node constructor

        @param data node data object
        """
        self.order = order
        self.vms = vms
        self.cpu_sum = 0.0
        self.mem_sum = 0.0
        #(flow_sum_inside, flow_sum_out)
        self.flow_sum = (0, 0)
        self.intra_flow = 0.0
    
    