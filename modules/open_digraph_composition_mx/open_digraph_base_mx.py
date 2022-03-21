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


class open_digraph_base_mx:
    def __init__(self, inputs: List[int], outputs: List[int], nodes: List[node]) -> None:
        '''
        __________________________
        Attributs:

        inputs: int list; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        __________________________
        '''
        self.inputs = inputs
        self.outputs = outputs
        self.nodes = {node.id:node for node in nodes} # self.nodes: <int,node> Dict

    def __str__(self) -> str:
        res = ""
        for node in self.nodes.values():
            for childrenID in node.children:
                res += node.label + " -(" + str(node.children[childrenID]) + ")-> " + self.nodes[childrenID].label + "\n"
        return res

    def __repr__(self) -> str:
        return f'open_digraph({self.inputs}, {self.outputs}, {self.nodes})'

    #getters
    
    def get_input_ids(self) -> List[int]:
        return self.inputs
    
    def get_output_ids(self) -> List[int]:
        return self.outputs
    
    def get_id_node_map(self) -> Dict[int, node]:
        return self.nodes
    
    def get_nodes(self) -> List[node]:
        return list(self.nodes.values())
    
    def get_node_ids(self) -> List[int]:
        return list(self.nodes.keys())
    
    def get_node_by_id(self, id: int) -> node:
        '''
        __________________________
        Parametre:

        id: int; the id of the wanted node
        __________________________
        '''
        if id in self.nodes:
            return self.nodes[id]
    
    def get_nodes_by_ids(self, ids: List[int]) -> List[node]:
        '''
        __________________________
        Parametre:

        ids: int list; the ids of the wanted nodes
        __________________________
        '''
        nodes = []
        for id in ids:
            if id in self.nodes:
                nodes.append(self.nodes[id])
        return nodes
    
    #setters
    def set_input_ids(self, input_ids: List[int]) -> None:
        '''
        __________________________
        Parametre:

        input_ids: int list; the ids of the new input nodes
        __________________________
        '''
        self.inputs = input_ids
    
    def set_output_ids(self, output_ids: List[int]) -> None:
        '''
        __________________________
        Parametre:

        output_ids: int list; the ids of the new output nodes
        __________________________
        '''
        self.outputs = output_ids
    
    def add_input_id(self, input_id: int) -> None:
        '''
        __________________________
        Parametre:

        input_id: int; the id of the new input node
        __________________________
        '''
        if not(input_id in self.inputs):
            raise ValueError("input ID is not in registered in inputs nodes")
        self.inputs.append(input_id)
    
    def add_output_id(self, output_id: int) -> None:
        '''
        __________________________
        Parametre:

        output_id: int; the id of the new output node
        __________________________
        '''
        if not(output_id in self.outputs):
            raise ValueError("output IDis not in registered in outputs nodes ")
        self.outputs.append(output_id)
    