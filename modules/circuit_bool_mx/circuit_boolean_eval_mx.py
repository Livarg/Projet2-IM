import sys
import os

root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)
from modules.matrix import *
from modules.node import *
from modules.open_digraph import *

class circuit_boolean_eval_mx:
    
    def copy_gate(self, Id : int):
        node = self.get_node_by_id(Id)
        if node.get_label() != "1" and node.get_label() != "0":
            raise ValueError("invalid pattern")
        idChild = node.get_children_ids()[0]
        copyChild = self.get_node_by_id(idChild)
        if copyChild.get_label() != '':
            raise ValueError("invalid pattern")
        for child in copyChild.get_children_ids:
            n = self.add_node(node.get_label)
            self.add_edge(n, child)
        self.remove_nodes_by_id(Id, idChild)