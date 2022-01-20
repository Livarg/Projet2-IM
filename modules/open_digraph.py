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
        '''
        id: int; the new id of the node
        '''
        self.id = id
    
    def set_label(self, label):
        '''
        label: string; the new label of the node
        '''
        self.label = label
    
    def set_parent_ids(self, parent_ids):
        '''
        parent_ids: int->int dict; the new parents of the node
        '''
        self.parents = parent_ids
    
    def set_children_ids(self, children_ids):
        '''
        children_ids: int->int dict; the new children of the node
        '''
        self.children = children_ids
    
    def add_child_id(self, child_id, mult):
        '''
        child_id: int; the id of the new child of the node
        mult: int; the multiplicity of the child
        '''
        if not(child_id in self.children):
            self.children[child_id] = mult
    
    def add_parent_id(self, parent_id, mult):
        '''
        parent_id: int; the id of the new parent of the node
        mult: int; the multiplicity of the parent
        '''
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
        self.max_id = 0
        for node in nodes:
            if node.get_id() > self.max_id:
                self.max_id = node.get_id()

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
        '''
        id: int; the id of the wanted node
        '''
        if id in self.nodes:
            return self.nodes[id]
    
    def get_nodes_by_ids(self, ids):
        '''
        ids: int list; the ids of the wanted nodes
        '''
        nodes = []
        for id in ids:
            if id in self.nodes:
                nodes.append(self.nodes[id])
        return nodes
    
    #setters
    def set_input_ids(self, input_ids):
        '''
        input_ids: int list; the ids of the new input nodes
        '''
        self.inputs = input_ids
    
    def set_output_ids(self, output_ids):
        '''
        output_ids: int list; the ids of the new output nodes
        '''
        self.outputs = output_ids
    
    def add_input_id(self, input_id):
        '''
        input_id: int; the id of the new input node
        '''
        if not(input_id in self.inputs):
            self.inputs.append(input_id)
            return 0
        return 1
    
    def add_output_id(self, output_id):
        '''
        output_id: int; the id of the new output node
        '''
        if not(output_id in self.outputs):
            self.outputs.append(output_id)
            return 0
        return 1
    

    def new_id(self):
        return self.max_id + 1
    
    def add_edge(self, src, tgt):
        '''
        src: int; the id of the parent in the new edge
        tgt: int; the id of the child in the new edge
        '''
        if not(src in self.nodes) or not(tgt in self.nodes):
            return 1
        src_node = self.get_node_by_id(src)
        tgt_node = self.get_node_by_id(tgt)

        if tgt in src_node.children:
            src_node.children[tgt] += 1
        else:
            src_node.children[tgt] = 1
        
        if src in tgt_node.parents:
            tgt_node.parents[src] += 1
        else:
            tgt_node.parents[src] = 1
        
        return 0
    
    def add_node(self, label='', parents={}, children={}):
        '''
        label: string; the label of the new node
        parents: int->int dict; maps a parent node's id to its multiplicity
        children: int->int dict; maps a child node's id to its multiplicity
        '''
        new_id = self.new_id()
        self.max_id += 1
        new_node = node(new_id, label, {}, {})
        self.nodes[new_id] = new_node

        for parent_id in parents:
            for _ in range(parents[parent_id]):
                self.add_edge(parent_id, new_id)
        
        for children_id in children:
            for _ in range(children[children_id]):
                self.add_edge(new_id, children_id)
            
        
    

    
