from doctest import FAIL_FAST
from multiprocessing.managers import ValueProxy
import string
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
from modules.open_digraph import *

class bool_circ(open_digraph) :
    
    def __init__(self, graph) -> None:
        super().__init__(graph.get_input_ids,graph.get_output_ids,graph.get_nodes)
        if not self.is_well_formed():
            raise ValueError("ce graph n'est pas un circuit booleen")
        
    """boolean circles are an extension of open digraphs """
    def __init__(self, inputs: List[int], outputs: List[int], nodes: List[node]) -> None:
        super().__init__(inputs, outputs, nodes)
        if not self.is_well_formed():
            raise ValueError("ce graph n'est pas un circuit booleen")
 

    def is_well_formed(self) -> bool :
        if self.is_cyclic():
            return False 
        for node in self.nodes.values() :
            if node.label == "" and node.indegree() > 1:
                return False
            if (node.label == "&" or node.label == "|") and node.outdegree() > 1:
                return False
            if node.label == "~" and (node.indegree() > 1 or node.outdegree() > 1):
                return False
        return True
    
    def pars_parenthese(*args):
        g = bool_circ([],[],[])
        for s in args:
            g.add_node('', {}, {})
            outID = g.max_id()
            g.add_node('', {g.max_id():1}, {})
            current_node = outID
            s2 = ''
            for char in s:
                if(char == '('):
                    tmp = g.get_node_by_id(current_node)
                    tmp.set_label(tmp.get_label() + s2)
                    g.add_node('', {}, {current_node:1})
                    current_node = g.max_id()
                    s2 = ''
                elif(char == ')'):
                    tmp = g.get_node_by_id(current_node)
                    tmp.set_label(tmp.get_label() + s2)
                    current_node = g.get_node_by_id(current_node).get_children_ids()[0]
                    s2 = ''
                else:
                    s2 += char
        labels = {}
        for obj in g.get_nodes():
            if(len(obj.get_parents_ids()) == 0):
                if obj.get_label() in labels:
                    g.fusion_node(g.get_node_by_id(labels[obj.get_label()]), obj )
                else:
                    labels[obj.get_label()] = obj.get_id()
        return g

    
    
            
                