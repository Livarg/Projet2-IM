from doctest import FAIL_FAST
from multiprocessing.managers import ValueProxy
from typing import Dict, List, Tuple
from logging import raiseExceptions
from random import choice
import sys
import os
from xml.dom.minicompat import NodeList

root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)
from modules.matrix import *
from modules.node import *

class open_digraph_methode_mx:
    def new_id(self) -> int:
        '''
        __________________________
        return: renvoie une nouvelle ID disponible
        __________________________
        '''
        return self.max_id + 1
    
    def add_edge(self, src: int, tgt: int) -> None:
        '''
        __________________________
        Parametre:

        src: int; the id of the parent in the new edge
        tgt: int; the id of the child in the new edge
        __________________________
        Methode:

        Add a link (arête) between two nodes
        __________________________
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
    
    def add_node(self, label: str = '', parents: Dict[int, int] = {}, children: Dict[int, int] = {}) -> None:
        '''
        __________________________
        Parametre:

        label: string; the label of the new node
        parents: int->int Dict; maps a parent node's id to its multiplicity
        children: int->int Dict; maps a child node's id to its multiplicity
        __________________________
        Methode:

        Add a node to the graph
        __________________________
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
            
    def remove_edge(self, src: int, tgt: int) -> None:
        '''
        __________________________
        Parametre:

        src: int; the id of the parent in the new edge
        tgt: int; the id of the child in the new edge
        __________________________
        Methode:

        Remove one link (arete) between two nodes
        __________________________
        '''
        self.nodes[src].remove_child_once(tgt)
        self.nodes[tgt].remove_parent_once(src)

    def remove_parallel_edge(self, src: int, tgt: int) -> None:
        '''
        __________________________
        Parametre:

        src: int; the id of the parent in the new edge
        tgt: int; the id of the child in the new edge
        __________________________
        Methode:

        Remove all links (arete) between two nodes
        __________________________
        '''
        self.nodes[src].remove_child_id(tgt)
        self.nodes[tgt].remove_parent_id(src)

    def remove_node_by_id(self, node_id: int) -> None:
        '''
        __________________________
        Parametre:

        node_id : int; representing the number of identification of a node
        __________________________
        Methode:

        Remove all links between a node and it's neighbours
        __________________________
        '''
        parents = self.nodes[node_id].get_parents_ids()
        for parent in parents:
            self.remove_parallel_edge(parent, node_id)
            if parent in self.inputs:
                self.inputs.remove(parent)
                self.nodes.pop(parent)
        
        children = self.nodes[node_id].get_children_ids()
        for child in children:
            self.remove_parallel_edge(node_id, child)
            if child in self.outputs:
                self.outputs.remove(child)
                self.nodes.pop(child)
        
        if node_id in self.inputs:
            self.inputs.remove(node_id)
        if node_id in self.outputs:
            self.outputs.remove(node_id)
        self.nodes.pop(node_id)

    def remove_nodes_by_id(self, nodes_id: List[int]) -> None:
        '''
        __________________________
        Parametre:

        nodes_id : int list; representing the number of identification of the nodes
        __________________________
        Methode:

        Remove all links between the nodes in nodes_id and their neighbours
        __________________________
        '''
        ids = nodes_id.copy()
        for id in ids:
            self.remove_node_by_id(id)

    def remove_edges(self, *args: List[Tuple[int, int]]) -> None:
        '''
        __________________________
        Parametre:

        *args : *tuple; representing the node source and node target
        __________________________
        Methode:

        Remove a link between the node source and the node target            
        __________________________
        '''
        for arg in args:
            if isinstance(arg, (list,tuple)):
                self.remove_edge(arg[0],arg[1])

    def remove_parallel_edges(self, *args: List[Tuple[int, int]]) -> None:
        '''
        __________________________
        Parametre:

        *args : *tuple; representing the node source and node target
        __________________________
        Methode:

        Remove all links between the node source and the node target            
        __________________________
        '''
        for arg in args:
            if isinstance(arg, (list,tuple)):
                self.remove_parallel_edge(arg[0],arg[1])
    
    def is_well_formed(self) -> bool:
        '''
        __________________________
        Methode:

        Check if all the propreties of a graph are respected
        __________________________
        '''
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
    
    def add_input_node(self, id: int) -> None:
        '''
        __________________________
        Parametre:

        id : int; number of identification of a node
        __________________________
        Methode:

        add a new input node if the node isn't pointing another input node
        __________________________
        '''
        if id in self.get_input_ids():
            raise ValueError("Input node can't point to another input node")
        new_id = self.new_id()
        self.add_node(str(new_id), {}, {id:1})
        self.inputs.append(new_id)
    
    def add_output_node(self, id: int) -> None:
        '''
        Parametre:

        id : int; number of identification of a node
        __________________________
        Methode:

        add a new output node if the node isn't pointing another output node
        __________________________
        '''
        if id in self.get_output_ids():
            raise ValueError("Output node can't point to another output node")
        new_id = self.new_id()
        self.add_node(str(new_id), {id:1}, {})
        self.outputs.append(new_id)
