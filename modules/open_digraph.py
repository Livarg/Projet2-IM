from doctest import FAIL_FAST
from logging import raiseExceptions
import re


class node:
    def __init__(self, identity, label, parents, children):
        '''
        Class node:

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
        """
        Méthode permettant de crée une copie d'une node
        """
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

    def remove_parent_once(self, parent_id):
        """
        Paramètres:
        parent_id : le numéro d'identification d'une node

        Modification:
        Vérifie que l'id rentré appartient au node parent de la node actuelle
        Si oui retire un lien entre les nodes
        """
        if not(parent_id in self.parents):
            raise ValueError("Le parents n'existe pas!")
        else :
            self.parents[parent_id] -= 1
        if (self.parents[parent_id] == 0):
            self.parents.pop(parent_id)

    def remove_parent_id(self, parent_id):
        """
        Paramètres:
        parent_id : le numéro d'identification d'une node

        Modification:
        Vérifie que l'id rentré appartient au node parent de la node actuelle
        Si oui retire tous les liens entre les nodes
        """
        if not(parent_id in self.parents):
            raise ValueError("Le parents n'existe pas!")
        else:
            self.parents.pop(parent_id)

    def remove_child_once(self, child_id):
        """
        Paramètres:
        child_id : le numéro d'identification d'une node

        Modification:
        Vérifie que l'id rentré appartient au node enfant de la node actuelle
        Si oui retire un liens entre les nodes
        """
        if not(child_id in self.children):
            raise ValueError("L'enfant n'existe pas!")
        else :
            self.children[child_id] -= 1
        if (self.children[child_id] == 0):
            self.children.pop(child_id)

    def remove_child_id(self, child_id):
        """
        Paramètres:
        child_id : le numéro d'identification d'une node

        Modification:
        Vérifie que l'id rentré appartient au node enfant de la node actuelle
        Si oui retire tous les liens entre les nodes
        """
        if not(child_id in self.children):
            raise ValueError("L'enfant n'existe pas!")
        else :
            self.children.pop(child_id)

        

    



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
                res += node.label + " -" + str(node.children[childrenID]) + "-> " + self.nodes[childrenID].label + "\n"
        return res

    def __repr__(self):
        return f'open_digraph({self.inputs}, {self.outputs}, {self.nodes})'

    def copy(self):
        """
        Méthode permettant de crée une copie d'un graph
        """
        nodes = []
        for node in self.nodes.values():
            nodes.append(node)
        _copy = open_digraph(self.inputs.copy(), self.outputs.copy(), nodes)
        return _copy

    @classmethod
    def empty(self):
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
        Paramètre :
        src: int; the id of the parent in the new edge
        tgt: int; the id of the child in the new edge

        Modification :
        Add a link (arête) between two nodes
        '''
        if not(src in self.nodes) or not(tgt in self.nodes):
            raise ValueError("Src or Tgt is not in the attribute nodes")
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
    
    def add_node(self, label='', parents={}, children={}):
        '''
        Paramètres :
        label: string; the label of the new node
        parents: int->int dict; maps a parent node's id to its multiplicity
        children: int->int dict; maps a child node's id to its multiplicity

        Modification :
        
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
            
    def remove_edge(self, src, tgt):
        self.nodes[src].remove_child_once(tgt)
        self.nodes[tgt].remove_parent_once(src)

    def remove_parallel_edge(self, src, tgt):
        self.nodes[src].remove_child_id(tgt)
        self.nodes[tgt].remove_parent_id(src)

    def remove_node_by_id(self, node_id):
        parents = self.nodes[node_id].get_parents_ids()
        for parent in parents:
            self.remove_parallel_edge(parent, node_id)
            if parent in self.inputs:
                self.inputs.remove(parent)
                self.nodes.pop(parent)
        
        children = self.nodes[node_id].get_children_ids()
        for child in children:
            print(child)
            self.remove_parallel_edge(node_id, child)
            if child in self.outputs:
                self.outputs.remove(child)
                self.nodes.pop(child)
        
        if node_id in self.inputs:
            self.inputs.remove(node_id)
        if node_id in self.outputs:
            self.outputs.remove(node_id)
        self.nodes.pop(node_id)

    def remove_nodes_by_id(self, nodes_id):
        for id in nodes_id:
            self.remove_node_by_id(id)

    def remove_edges(self, *args):
        for arg in args:
            if isinstance(arg, (list,tuple)):
                self.remove_edge(arg[0],arg[1])

    def remove_parallel_edges(self, *args):
        for arg in args:
            if isinstance(arg, (list,tuple)):
                self.remove_parallel_edge(arg[0],arg[1])
    
    def is_well_formed(self):
        for input_id in self.inputs:
            # TEST 1
            if not(input_id in self.nodes):
                return False
            # TEST 2
            if len( self.nodes[input_id].get_parents_ids() ) != 0 or len( self.nodes[input_id].get_children_ids() ) != 1:
                return False
            if list(self.nodes[input_id].children.values())[0] != 1:
                return False
        
        for output_id in self.outputs:
            # TEST 1
            if not(output_id in self.nodes):
                return False
            # TEST 3
            if len( self.nodes[output_id].get_parents_ids() ) != 1 or len( self.nodes[output_id].get_children_ids() ) != 0:
                return False
            if list(self.nodes[output_id].parents.values())[0] != 1:
                return False
        
        for node_id in self.nodes:
            # TEST 4
            if self.nodes[node_id].get_id() != node_id:
                return False
            
            # TEST 5
            for parent_id in self.nodes[node_id].get_parents_ids():
                if self.nodes[node_id].parents[parent_id] != self.nodes[parent_id].children[node_id]:
                    return False
            for children_id in self.nodes[node_id].get_children_ids():
                if self.nodes[node_id].children[children_id] != self.nodes[children_id].parents[node_id]:
                    return False
        return True
    
    def add_input_node(self, id):
        if id in self.get_input_ids():
            raise ValueError("Input node can't point to another input node")
        new_id = self.new_id()
        self.add_node('', {}, {id:1})
        self.inputs.append(new_id)
    
    def add_output_node(self, id):
        if id in self.get_output_ids():
            raise ValueError("Output node can't point to another output node")
        new_id = self.new_id()
        self.add_node('', {id:1}, {})
        self.outputs.append(new_id)

    
