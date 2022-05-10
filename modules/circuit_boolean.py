from doctest import FAIL_FAST
from lib2to3.pytree import Node
from multiprocessing.managers import ValueProxy
import string
from typing import Dict, List, Tuple
from logging import raiseExceptions
from random import choice
from math import log, ceil
import sys
import os
from xml.dom.minicompat import NodeList

root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)
from modules.matrix import *
from modules.node import *
from modules.open_digraph import *
from modules.circuit_bool_mx.circuit_boolean_eval_mx import *

class bool_circ(open_digraph,circuit_boolean_eval_mx) :
    
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
            if (node.label == "&" or node.label == "|" or node.label == "^") and node.outdegree() > 1:
                return False
            if node.label == "~" and (node.indegree() > 1 or node.outdegree() > 1):
                return False
        return True
    
    def pars_parenthese(*args):
        g = bool_circ([],[],[])
        logic = ['~','|','&', '']
        for s in args:
            g.add_node('', {}, {})
            outID = g.max_id()
            g.add_node('', {g.max_id():1}, {})
            g.add_output_id(g.max_id())
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
            if not(obj.get_label() in logic):
                if obj.get_label() in labels:
                    g.fusion_node(g.get_node_by_id(labels[obj.get_label()]), obj )
                else:
                    labels[obj.get_label()] = obj.get_id()
        for obj in g.get_nodes():
            if not(obj.get_label() in logic):
                g.add_node(obj.get_label(), {}, {obj.get_id() : 1})
                g.add_input_id(g.max_id())
        return g
                
    def circuit_from_int(n):
        b = bin(n)
        len_b = len(b) - 2
        nb_inputs = ceil(log(len_b, 2))
        tmp = ["0" for _ in range(2**nb_inputs - len_b)]
        binary = "".join(tmp) + b[2:]
        print(nb_inputs)
        print(binary)
        list_input = []
        list_bin_input = []
        list_nodes = []
        for i in range(nb_inputs):
            node1 = node(2*i, str(i), {}, {(2*i+1) : 1})
            node2 = node(2*i+1, "", {(2*i) : 1}, {})
            list_input.append(node1.get_id())
            list_bin_input.append(node2.get_id())
            list_nodes.append(node1)
            list_nodes.append(node2)
        node_output = node(2*nb_inputs+2, "", {2*nb_inputs+3 : 1}, {})
        node_bin_output = node(2*nb_inputs+3, "|", {}, {2*nb_inputs+2 : 1})
        circ = bool_circ(list_input, [node_output.get_id()], list_nodes + [node_output, node_bin_output])
        
        for i, b in enumerate(binary):
            print(i,b,binary)
            if int(b):
                circ.add_node("&", {}, {node_bin_output.get_id() : 1})
                node_and = circ.max_id()
                bin_i = bin(i)
                tmp = ["0" for _ in range(nb_inputs - (len(bin_i) - 2))]
                bin_i = "".join(tmp) + bin_i[2:]
                for i2, b2 in enumerate(bin_i):
                    if not(int(b2)):
                        circ.add_node("~", {list_bin_input[i2] : 1}, {node_and : 1})
                    else:
                        circ.add_edge(list_bin_input[i2], node_and)
        return circ
    
    def random_bool_circ(n, nb_input, nb_output):
        if(nb_input < 1 or nb_output < 1):
            raise ValueError("Il faut impérativement une input et une output")
        ope_bin = ['&','|']
        ope_un =['~','']
        circ = open_digraph.random_graph(n,2,0,0,"DAG")
        top_node = []
        bottom_node = []
        for node in circ.get_nodes():
            if len(node.get_parents_ids()) == 0:
                top_node.append(node)
            
            if len(node.get_children_ids()) == 0:
                bottom_node.append(node)
                
        for node in top_node:
         #   circ.add_node('',{},{node.get_id():1})
            circ.add_input_node(node.get_id())
        
        for node in bottom_node:
         #   circ.add_node('',{node.get_id():1},{})
            circ.add_output_node(node.get_id())
        
        nodes = circ.get_node_ids()
        """
        for i in range(nb_input - len(circ.get_input_ids())):
            node = choice(nodes)
            while node in circ.get_input_ids():
                node = choice(nodes)
            circ.add_node('', {}, { node:1})
            circ.add_input_node(circ.max_id())
        
        while nb_input < len(circ.get_input_ids()):
            node1 = choice(circ.get_input_ids())
            node2 = node1
            while node2 == node1:
                node2 = choice(circ.get_input_ids())
            circ.add_node('', {node2 : 1}, {circ.get_node_by_id(node1).get_children_ids()[0] : 1, circ.get_node_by_id(node2).get_children_ids()[0] : 1})
            circ.remove_node_by_id(node1)
        """
        for i in range(nb_output - len(circ.get_output_ids())):
            node = choice(nodes)
            while node in circ.get_output_ids():
                node = choice(nodes)
            circ.add_node('', {node : 1}, {})
            circ.add_output_node(circ.max_id())
        
        while nb_output < len(circ.get_output_ids()):
            node1 = choice(circ.get_output_ids())
            node2 = node1
            while node2 == node1:
                node2 = choice(circ.get_output_ids())
            circ.add_node('', {circ.get_node_by_id(node1).get_parents_ids()[0] : 1, circ.get_node_by_id(node2).get_parents_ids()[0] : 1}, {node2 : 1})
            circ.remove_node_by_id(node1)
        
        for node in circ.get_nodes():
            if(len(node.get_children_ids()) == 1 and len(node.get_parents_ids()) == 1):
                node.set_label(choice(ope_un))
            elif(len(node.get_children_ids()) == 1 and len(node.get_parents_ids()) > 1):
                node.set_label(choice(ope_bin))
            elif(len(node.get_children_ids()) > 1 and len(node.get_parents_ids()) == 1):
                node.set_label('')
            elif(len(node.get_children_ids()) > 1 and len(node.get_parents_ids()) > 1):
                circ.add_node('',{},node.children.copy())
                #print([[node.get_id(), child_id] for child_id in node.get_children_ids()])
                circ.remove_edges(*[[node.get_id(), child_id] for child_id in node.get_children_ids()])
                node.set_label(choice(ope_bin))
                circ.add_edge(node.get_id(), circ.max_id())
                
        return circ
    
    # Il faut faire les adder
    def adder(a : string, b : string, carry : string = '0') -> open_digraph:
        m = max(len(a), len(b))
        n = ceil(log(m, 2))

        a = '0'*(n - len(a)) + a
        b = '0'*(n - len(b)) + b

        if n == 0:
            G = bool_circ.empty()

            G.add_node('a')
            mult1 = G.max_id()
            G.add_node('b')
            mult2 = G.max_id()
            G.add_node('c')
            mult3 = G.max_id()
            G.add_node('^', {mult1 : 1, mult2 : 1})
            xor1 = G.max_id()
            G.add_node('&', {mult1 : 1, mult2 : 1})
            and1 = G.max_id()
            G.add_node('', {xor1 : 1})
            mult4 = G.max_id()
            G.add_node('&', {mult4 : 1, mult3 : 1})
            and2 = G.max_id()
            G.add_node('|', {and1 : 1, and2 : 1})
            or1 = G.max_id()
            G.add_node('^', {mult4 : 1, mult3 : 1})
            xor2 = G.max_id()
            G.add_output_node(or1, 'c')
            G.add_output_node(xor2, 'out')
            G.add_input_node(mult1)
            G.add_input_node(mult2)
            G.add_input_node(mult3)

            inputs = G.get_input_ids()
            for i in range(len(inputs)):
                G.get_node_by_id(inputs[i]).set_label(str(i) +' '+ (a+b+carry)[i])

            outputs = G.get_output_ids()
            for i in range(len(outputs)):
                G.get_node_by_id(outputs[i]).set_label(str(i))

            return G


        G1 = bool_circ.adder(b[:len(b)//2], b[len(b)//2:], carry)
        #G1.add_input_node(G1.get_node_ids()[0])
        G2 = bool_circ.adder(a[:len(a)//2], a[len(a)//2:])

        G1.iparallel(G2)

        
        c2_input = G2.get_node_by_id(G2.get_input_ids()[-1])
        c2_in_node_id = c2_input.get_children_ids()[0]
        G1.remove_node_by_id(c2_input.get_id())

        c1_output = G1.get_node_by_id(G1.get_output_ids()[0])
        c1_out_node_id = c1_output.get_parents_ids()[0]
        G1.remove_node_by_id(c1_output.get_id())

        G1.add_edge(c1_out_node_id, c2_in_node_id)

        l = 2**(n-1)
        inputs = G1.get_input_ids()
        # pour n = 1 on a pour i index de inputs 
        # G1 0-1    c 2    G2 3-4
        # et on veux
        # G2a 0    G1a 1    G2b 2    G1b 3    c 4
        a1 = inputs[:l]
        b1 = inputs[l:2*l]
        c = inputs[2*l:2*l+1]
        a2 = inputs[2*l+1:3*l+1]
        b2 = inputs[3*l+1:]
        inputs = a2 + a1 + b2 + b1 + c
        G1.set_input_ids(inputs)

        outputs = G1.get_output_ids()
        # pour n = 1 on a pour les outputs
        # G1o 0    c 1    G2o 2
        # et on veux
        # c    G2o 1    G1o 2
        o1 = outputs[:l]
        c = outputs[l:l+1]
        o2 = outputs[l+1:]
        print(outputs)
        print(o1,c,o2)
        outputs = c + o2 + o1
        G1.set_output_ids(outputs)

        # pour debug ou voir dans quel ordre lire les nombres binaires
        for i in range(len(inputs)):
            G1.get_node_by_id(inputs[i]).set_label(str(i) +' '+ (a+b+carry)[i])
        
        for i in range(len(outputs)):
            G1.get_node_by_id(outputs[i]).set_label(str(i))

        return G1

    def half_adder(a : string, b : string) -> open_digraph:
        G = bool_circ.adder(a, b)
        carry = G.get_node_by_id(G.get_input_ids()[-1])
        carry.set_label("0")
        G.set_input_ids(G.get_input_ids()[:-1])
        return G

def int_to_boolCirc(self, val : int, n : int = 8):
    bites = bin(val)[2:]
    if len(bites) > n:
        raise ValueError("This number is too big")
    bites = "0" * (int(n - len(bites))) + bites
    graph = open_digraph.empty()
    for bit in bites:
        num = graph.add_node(bit)
        graph.add_output_node(num)
    return graph
    