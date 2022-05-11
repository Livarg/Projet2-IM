import sys
import os

from numpy import true_divide

root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)
from modules.matrix import *
from modules.node import *
from modules.open_digraph import *

class circuit_boolean_eval_mx:
    
    def copy_gate(self, Id : int):
        node = self.get_node_by_id(Id)
        if node.get_label() != "1" and node.get_label() != "0":
            raise ValueError("invalid pattern label != 0/1")
        idChild = node.get_children_ids()[0]
        child = self.get_node_by_id(idChild)
        if child.get_label() != '':
            raise ValueError("invalid pattern label != ''")
        for c in child.get_children_ids():
            n = self.add_node(node.get_label())
            self.add_edge(n, c)
        self.remove_nodes_by_id([Id, idChild])
        
    def not_gate(self, ID : int):
        node = self.get_node_by_id(ID)
        if(self.get_node_by_id(node.get_children_ids()[0]).get_label() != "~"):
            raise ValueError("invalid pattern")
        child = self.get_node_by_id(node.get_children_ids()[0])
        if(node.get_label() == "0"):
            child.set_label("1")
        elif(node.get_label() == "1"):
            child.set_label("0")
        else:
            raise ValueError("invalid pattern")
        self.remove_nodes_by_id(ID)
        
    def and_gate(self, Id: int):
        node = self.get_node_by_id(Id)
        label = node.get_label()
        if label != "1" and label != "0":
            raise ValueError("invalid pattern")
        idChild = node.get_children_ids()[0]
        child = self.get_node_by_id(idChild)
        if child.get_label() != '&':
            raise ValueError("invalid pattern")
        if label == "0":
            for parent in child.get_parent_ids():
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
        label = node.get_label()
        if label != "1" and label != "0":
            raise ValueError("invalid pattern")
        idChild = node.get_children_ids()[0]
        child = self.get_node_by_id(idChild)
        if child.get_label() != '|':
            raise ValueError("invalid pattern")
        if label == "1":
            for parent in child.get_parent_ids():
                if parent != ID:
                    n = self.add_node('')
                    self.add_edge(parent, n)
                    self.remove_edge(parent, idChild)
            child.set_label("1")
            self.remove_nodes_by_id(ID)
        if label == "0":
            self.remove_node_by_id(ID)
            
    def xor_gate(self, ID: int):
        node = self.get_node_by_id(id)
        if self.get_node_by_id(node.get_children_ids()[0]).get_label() != "^":
            raise ValueError("invalid pattern")
        if node.get_label() == "1":
            child = self.get_node_by_id(node.get_children_ids()[0])
            idChild = self.add_node("~")
            self.add_edges((child.get_id(), idChild),
                           (idChild, child.get_children_ids()[0]))
            self.remove_edge(child.get_id(), child.get_children_ids()[0])

        elif node.get_label() != "0":
            raise ValueError("invalid pattern")

        self.remove_nodes_by_id(ID)
        
    def neutre_gate(self, id: int):
        node = self.get_node_by_id(id)
        if len(node.get_parent_ids()) > 0:
            raise ValueError("invalid pattern")
        if (node.get_label()== "|" or node.get_label() == "^"):
            node.set_label("0")
        elif node.get_label() == "&":
            node.set_label("1")
        else:
            raise ValueError("invalid pattern")
        
    def evaluate(self):
        run = True
        while run:
            run = False
            for ID in self.get_node_ids():
                node = self.get_node_by_id(ID)
                if node != None and len(node.get_parents_ids()) == 0:
                    self.remove_node_by_id(ID)
                elif((node.get_label() != "0" and node.get_label() != "1") or node.get_children_ids()[0] not in self.get_output_ids()):
                        node = self.get_node_by_id(ID)
                        if node.get_label() == '&' or node.get_label() == '|' or node.get_label() == '^':
                            self.neutre_gate(ID)
                        else:
                            children = node.get_children_ids()
                            if len(children) != 1:
                                raise ValueError("too many children ;(")
                            label = self.get_node_by_id(children[0]).get_label()
                            if label == '':
                                self.copy_gate(ID)
                            elif label == '&':
                                self.and_gate(ID)
                            elif label == '|':
                                self.or_gate(ID)
                            elif label == '~':
                                self.not_gate(ID)
                            elif label == '^':
                                self.xor_gate(ID)
                        run = True