import re


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

    def __str__(self):
        parents = "[ "
        children = "[ "
        for parentID in self.parents:
            parents += f'{parentID}, '
        parents += "]"
        for childrenID in self.children:
            children += f'{childrenID}, '
        children += "]"
        res = f"Name : {self.label}; ID = {self.id}; Parents : {parents}; Children : {children}"
        return res
    
    def __repr__(self):
        return f'node({self.id}, "{self.label}", {self.parents}, {self.children})'
    
    def copy(self):
        copyParents = {nodeID:self.parents[nodeID] for nodeID in self.parents}
        copyChildren = {nodeID:self.children[nodeID] for nodeID in self.children}
        _copy = node(self.id, self.label, copyParents, copyChildren)
        return _copy
    
    #getters
    def get_id(self):
        return self.id
    
    def get_label(self):
        return self.label
    
    def get_parents_ids(self):
        return list(self.parents.keys())
    
    def get_children_ids(self):
        return list(self.children.keys())
    
    #setters
    def set_id(self, id):
        self.id = id
    
    def set_label(self, label):
        self.label = label
    
    def set_parent_ids(self, parent_ids):
        self.parents = parent_ids
    
    def set_children_ids(self, children_ids):
        self.children = children_ids
    
    def add_child_id(self, child_id, mult):
        if not(child_id in self.children):
            self.children[child_id] = mult
    
    def add_parent_id(self, parent_id, mult):
        if not(parent_id in self.parents):
            self.parents[parent_id] = mult
    



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
        for node in self.nodes.values():
            for childrenID in node.children:
                res += node.label + "->" + self.nodes[childrenID].label + "\n"
        return res

    def __repr__(self):
        return f'open_digraph({self.inputs}, {self.outputs}, {self.nodes})'

    def copy(self):
        nodes = []
        for node in self.nodes.values():
            nodes.append(node)
        _copy = open_digraph(self.inputs.copy(), self.outputs.copy(), nodes)
        return _copy

    @classmethod
    def empty(self):
        #self.inputs = []
        #self.outputs = []
        #self.nodes = []
        return open_digraph([],[],[])
    
    #getters
    def get_input_ids(self):
        return self.inputs
    
    def get_output_ids(self):
        return self.outputs
    
    def get_id_node_map(self):
        return self.nodes
    
    def get_nodes(self):
        return list(self.nodes.values())
    
    def get_node_ids(self):
        return list(self.nodes.keys())
    
    def get_node_by_id(self, id):
        return self.nodes[id]
    
    def get_nodes_by_ids(self, ids):
        nodes = []
        for id in ids:
            nodes.append(self.nodes[id])
        return nodes
    
    #setters
    def set_input_ids(self, input_ids):
        self.inputs = input_ids
    
    def set_output_ids(self, output_ids):
        self.outputs = output_ids
    
    def add_input_id(self, input_id):
        if not(input_id in self.inputs):
            self.inputs.append(input_id)
    
    def add_output_id(self, output_id):
        if not(output_id in self.outputs):
            self.outputs.append(output_id)
    
    
    
