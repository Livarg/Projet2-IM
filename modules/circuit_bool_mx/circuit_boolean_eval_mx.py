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
        child = self.get_node_by_id(idChild)
        if child.get_label() != '':
            raise ValueError("invalid pattern")
        for c in child.get_children_ids:
            n = self.add_node(node.get_label)
            self.add_edge(n, c)
        self.remove_nodes_by_id([Id, idChild])
        
    def not_gate(self, ID : int):
        node = self.get_node_by_id(ID)
        if(self.get_node_by_id(node.get_children_ids[0]).get_label != "~"):
            raise ValueError("invalid pattern")
        child = self.get_node_by_id(node.get_children_ids[0])
        if(node.get_label == "0"):
            child.set_label("1")
        elif(node.get_label == "1"):
            child.set_label("0")
        else:
            raise ValueError("invalid pattern")
        self.remove_nodes_by_id(ID)
        
    def and_gate(self, Id: int):
        node = self.get_node_by_id(Id)
        label = node.get_label
        if label != "1" and label != "0":
            raise ValueError("invalid pattern")
        idChild = node.get_children_ids[0]
        child = self.get_node_by_id(idChild)
        if child.get_label != '&':
            raise ValueError("invalid pattern")
        if label == "0":
            for parent in child.get_parent_ids:
                if parent != Id:
                    n = self.add_node('')
                    self.add_edge(parent, n)
                    self.remove_edge(parent, idChild)
            child.set_label("0")
            self.remove_nodes_by_id(id)
        if label == "1":
            self.remove_node_by_id(id)
            
    def or_gate(self, ID : int):
        node = self.get_node_by_id(ID)
        label = node.get_label
        if label != "1" and label != "0":
            raise ValueError("invalid pattern")
        idChild = node.get_children_ids[0]
        child = self.get_node_by_id(idChild)
        if child.get_label != '|':
            raise ValueError("invalid pattern")
        if label == "1":
            for parent in child.get_parent_ids:
                if parent != ID:
                    n = self.add_node('')
                    self.add_edge(parent, n)
                    self.remove_edge(parent, idChild)
            child.set_label("1")
            self.remove_nodes_by_id(ID)
        if label == "0":
            self.remove_node_by_id(ID)
            