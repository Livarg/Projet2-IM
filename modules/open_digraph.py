class node:
    def __init__(self, identity, label, parents, children):
        '''
        identity: int; its unique id in the graph
        label: string;
        parents: int->int dict; maps a parent node's id to its multiplicity
        children: int->int dict; maps a child node's id to its multiplicity
        '''
        self.id = identity
        self.label = label
        self.parents = parents
        self.children = children


class open_digraph: # for open directed graph
    def __init__(self, inputs, outputs, nodes):
        '''
        inputs: int list; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        '''
        self.inputs = inputs
        self.outputs = outputs
        self.nodes = {node.id:node for node in nodes} # self.nodes: <int,node> dict

    def __str__(self):
        res = ""
        for nodeID in self.nodes:
            for childrenID in self.nodes[nodeID].children:
                res += self.nodes[nodeID].label + "->" + self.nodes[childrenID].label + "\n"
        return res

    def __repr__(self):
        res = "[ "
        for nodeID in self.nodes:
            res += f'self.nodes[nodeID].id' + ", "
        return res + "] \n"

    @classmethod
    def empty(self):
        self.inputs = []
        self.outputs = []
        self.nodes = []