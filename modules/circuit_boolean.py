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
from modules.open_digraph import *

class bool_circ(open_digraph) :
    """boolean circles are an extension of open digraphs """
    def __init__(self, inputs: List[int], outputs: List[int], nodes: List[node]) -> None:
        super().__init__(inputs, outputs, nodes)
        if not self.is_well_formed():
            raise ValueError("ce graph n'est pas un circuit booleen")
    
    def __init__(self, graph) -> None:
        super().__init__(graph.get_inputs_ids,graph.get_output_ids,graph.get_nodes)
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