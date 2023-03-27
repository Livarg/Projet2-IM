import sys
import os

from numpy import true_divide

root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)
from modules.matrix import *
from modules.node import *
from modules.open_digraph import *

class circuit_boolean_eval_mx:
    
    def copy_gate(self, ID : int):
        node = self.get_node_by_id(ID)
        if node.get_label() != '':
            raise ValueError("invalid pattern label")
        if len(node.get_parents_ids()) == 1 and (node.get_parents_ids()[0] == "1" or node.get_parents_ids()[0] == "0"):
            for c in node.get_children_ids():
                n = self.add_node(node.get_parents_ids()[0].get_label())
                self.add_edge(n, c)
            self.remove_nodes_by_id([ID,node.get_parents_ids()[0]])
        
    def not_gate(self, ID : int):
        node = self.get_node_by_id(ID)
        if(node.get_label() != "~"):
            raise ValueError("invalid pattern")
        parent = self.get_node_by_id(node.get_parents_ids()[0])
        if(parent.get_label() == "0"):
            node.set_label("1")
        elif(parent.get_label() == "1"):
            node.set_label("0")
        else:
            raise ValueError("invalid pattern")
        #self.remove_nodes_by_id(self.get_node_by_id(node.get_parents_ids()[0]))
        self.remove_nodes_by_id(node.get_parents_ids()) 
            
    def and_gate(self, ID: int):
        node = self.get_node_by_id(ID)
        label = node.get_label()
        if label != "&":
            raise ValueError("invalid pattern")
        for parent in node.get_parents_ids():
            if self.get_node_by_id(parent).get_label() == "1":
                self.remove_nodes_by_id(parent)
            elif self.get_node_by_id(parent).get_label() == "0":
                node.set_label("0")
                for p in node.get_parents_ids():
                    self.remove_egdes(p,ID)
                    n = self.add_node('')
                    self.add_edge(p, n)
                
    def or_gate(self, ID : int):
        node = self.get_node_by_id(ID)
        label = node.get_label()
        if label != "|":
            raise ValueError("invalid pattern")
        for parent in node.get_parents_ids():
            if self.get_node_by_id(parent).get_label() == "0":
                self.remove_nodes_by_id(parent)
            elif self.get_node_by_id(parent).get_label() == "1":
                node.set_label("1")
                for p in node.get_parents_ids():
                    self.remove_egdes(p,ID)
                    n = self.add_node('')
                    self.add_edge(p, n)
                    
                    
    def xor_gate(self, ID: int):
        node = self.get_node_by_id(ID)
        label = node.get_label()
        if label != "^":
            raise ValueError("invalid pattern")
        for parent in node.get_parents_ids():
            if self.get_node_by_id(parent).get_label() == "0":
                self.remove_nodes_by_id(parent)
            elif self.get_node_by_id(parent).get_label() == "1":
                self.remove_nodes_by_id(parent)
                n = self.add_node('~',{},node.children)
                self.add_edge(ID, n)
                self.remove_edges(node, node.get_children_ids()[0])
        
    def neutre_gate(self, id: int):
        node = self.get_node_by_id(id)
        if len(node.get_parents_ids()) > 0:
            raise ValueError("invalid pattern")
        if (node.get_label()== "|" or node.get_label() == "^"):
            node.set_label("0")
        elif node.get_label() == "&":
            node.set_label("1")
        else:
            raise ValueError("invalid pattern")