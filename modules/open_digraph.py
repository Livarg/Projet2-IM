from doctest import FAIL_FAST
from multiprocessing.managers import ValueProxy
from tokenize import String
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
from modules.open_digraph_composition_mx.open_digraph_base_mx import *
from modules.open_digraph_composition_mx.open_digraph_methode_mx import *
from modules.open_digraph_composition_mx.open_digraph_distance_mx import *


class open_digraph(open_digraph_base_mx, open_digraph_methode_mx, open_digraph_distance_mx): # for open directed graph
    def copy(self):
        '''
        __________________________
        Methode:

        Créer une copie d'un graphe, la copie et l'original sont bien 2 instances différentes
        __________________________
        '''
        nodes = []
        for node in self.nodes.values():
            nodes.append(node.copy())
        _copy = open_digraph(self.inputs.copy(), self.outputs.copy(), nodes)
        return _copy

    @classmethod
    def empty(self):
        '''
        ___________________________
        Methode:
        
        Renvoie un open_digraph vide
        ___________________________
        '''
        return open_digraph([],[],[])
    

    @classmethod
    def graph_from_adjacency_matrix(self, matrix: List[List[int]]):
        '''
        __________________________
        Parametre:

        matrix : un double tableau d'entier qui possèdes des propriétés similaire a une matrice
        __________________________
        Methode:

        Créer un open-digraph a partir d'une matrice
        __________________________
        '''
        graph = self.empty()
        for i in range(len(matrix)):
            graph.add_node('')
        for x in range(len(matrix)):
            for y in range(len(matrix)):
                for _ in range(matrix[x][y]):
                    graph.add_edge(x,y)
        return graph

    @classmethod
    def random_graph(self, n: int, bound: int, inputs: int = 0, outputs: int = 0, form: str = "free"):
        '''
        ___________________________
        Parameters:

        n       : int; number of non input/output nodes
        bound   : int; max multiplicity number
        inputs  : int; number of input nodes
        outputs : int; number of output nodes
        form    : str; form of the graph :
                        "free"       : random digraph with no constrains
                        "DAG"        : Directed Acyclic Graph, random digraph with no cycles
                        "oriented"   : random digraph with no nodes pointing to each other
                        "loop-free"  : random digraph with no nodes pointing to themself
                        "undirected" : random graph with each connections being both ways
                        "loop-free undirected" : loop-free and undirected random graph
        __________________________
        Return:

        creates and return a random digraph with n inner nodes
        connected to each others with a random multiplicity between 0 and bound,
        inputs input nodes, outputs output nodes
        and a specific form if specified
        __________________________
        '''
        matrix = []
        if form=="free":
            matrix = random_int_matrix(n,bound, False)
        elif form=="DAG":
            matrix = random_triangular_int_matrix(n, bound)
        elif form=="oriented":
            matrix = random_oriented_matrix(n, bound)
        elif form=="loop-free":
            matrix = random_int_matrix(n, bound)
        elif form=="undirected":
            matrix = random_symetric_int_matrix(n, bound, False)
        elif form=="loop-free undirected":
            matrix = random_symetric_int_matrix(n, bound)
        
        graphe = self.graph_from_adjacency_matrix(matrix)
        node_ids = graphe.get_node_ids()
        for _ in range(inputs):
            graphe.add_input_node(choice(node_ids))
        for _ in range(outputs):
            graphe.add_output_node(choice(node_ids))
        return graphe
    
    def get_lower_ids(self) -> Dict[int, int]:
        '''
        __________________________
        Method:

        creates and return a Dictionnary who couple each node id
        with a unique number i such that if there is n nodes,
        0 <= i < n
        __________________________
        '''
        res = {}
        node_ids = self.get_node_ids()
        for i in range(len(node_ids)):
            res[node_ids[i]] = i
        return res

    def adjacency_matrix(self) -> List[List[int]]:
        '''
        __________________________
        Return:

        creates and return the adjacency matrix of the graph, ignoring inputs and outputs
        __________________________
        '''
        copy = self.copy()

        input_ids = copy.get_input_ids()
        output_ids = copy.get_output_ids()
        copy.remove_nodes_by_id(input_ids)
        copy.remove_nodes_by_id(output_ids)

        matrix_ids = copy.get_lower_ids()
        node_ids = copy.get_node_ids()
        n = len(node_ids)

        matrix = [[0 for _ in range(n)] for _ in range(n)]
        for parent in range(n):
            parent_id = matrix_ids[parent]
            children = copy.get_node_by_id(parent_id).children
            for child in range(n):
                child_id = matrix_ids[child]
                if child_id in children:
                    matrix[parent][child] = children[child_id]
                else:
                    matrix[parent][child] = 0
        return matrix
        
    def save_as_dot_file(self, path = os.getcwd(), verbose=False) -> None:
        '''
        __________________________
        Parametre:

        path : chemin vers le dossier dans le quel on travail
        __________________________
        Methode:

        Créer un fichier .dot a partir d'un open_digraph afin de le visualiser facilement
        __________________________
        '''
        file = open(path + "/Open_digraph.dot", "w+")
        file.writelines("digraph G { \n\n")
        for node in self.nodes.values() :
            for ID in node.children :
                for _ in range(node.children[ID]) : 
                    file.write("    " + str(node.get_id()) + "->" + str(self.nodes[ID].get_id()) + ";\n")
            if verbose :
                file.write("    " + str(node.get_id()) + "[label = \"" + node.get_label()  + "\"]; \n" )
            if node.get_id() in self.get_input_ids():
                file.write("    " + str(node.get_id()) + "[shape = Mdiamond, color = green];\n")
            if node.get_id() in self.get_output_ids():
                file.write("    " + str(node.get_id()) + "[shape = Msquare, color = red];\n")
        file.write("\n}")
        file.close()

    
    
    def from_dot_file(file_path, verbose=False):

        def get_next_word(line, i=0):
            n = len(line)
            space = [" ", "    "]
            spe_char = ["[", "]", "{", "}", "-", ">", ";", "=", ","]
            while i < n and line[i] in space:
                i += 1
            if i >= n:
                return "", i, 1
            if line[i] == "\n":
                return "", i, -1
            if line[i] in spe_char:
                return line[i], i+1, 2
            word = ""
            while i < n and not(line[i] in space) and not(line[i] in spe_char):
                word = word + line[i]
                i += 1
            return word, i, 0
        
        file = open(file_path, "r")
        G = open_digraph.empty()
        nodes = {}
        node_properties = {}
        inputs = []
        outputs = []
        for line in file:
            i = 0
            prev_word = ""
            prev_node = ""
            adding_properties = False
            while True:
                word, i, end = get_next_word(line, i)
                if end == -1: # end of line
                    #print("end line \\n")
                    break
                if end == 1:
                    #print("error i out of range")
                    break
                if end == 0: # the word is composed of letters
                    # Handling the first line
                    if word == "digraph":
                        word, i, end = get_next_word(line, i)
                        if word != "{":
                            word, i, end = get_next_word(line, i)
                            if word != "{":
                                raise ValueError("expected '{' after the name of the digraph")
                    else:
                        #print("word : " + word)
                        if adding_properties:
                            #print(node_properties)
                            if prev_node == "":
                                raise ValueError("missing node name to add properties to")
                            property_name = word
                            word, i, end = get_next_word(line, i)
                            if word != "=":
                                raise ValueError("property must get a value assigned with '='")
                            word, i, end = get_next_word(line, i)
                            if end != 0:
                                raise ValueError("missing property to add")
                            node_properties[prev_node][property_name] = word
                        
                        elif not word in nodes:
                            id = G.new_id()
                            label = word if verbose else ""
                            G.add_node(label)
                            nodes[word] = id
                            node_properties[word] = {}
                            prev_node = word
                            #print('prev node : ', prev_node)

                        else:
                            prev_node = word
                            #print('prev node :', prev_node)
                        prev_word = word
                        
                
                if end == 2: # word is a special character
                    #print("special char : " + word)
                    if word == "-":
                        word, i, end = get_next_word(line, i)
                        if word != ">":
                            raise ValueError("expected '>' after '-'")
                        word, i, end = get_next_word(line, i)
                        if end != 0:
                            raise ValueError("expected node name after '->'")
                        if prev_word == "":
                            raise ValueError("expected node name before '->'")
                        
                        #print("word : " + word)
                        if not word in nodes:
                            id = G.new_id()
                            label = word if verbose else ""
                            G.add_node(label)
                            nodes[word] = id
                            node_properties[word] = {}
                        #print(nodes)
                        #print(prev_node, word)
                        G.add_edge(nodes[prev_node], nodes[word])
                        prev_node = word
                        
                    
                    elif word == "[":
                        adding_properties = True
                    elif word == "]":
                        adding_properties = False
                    prev_word = word
        
        #print('\nread complete !\n')
        for node_name in nodes:
            node_ID = nodes[node_name]
            if verbose and 'label' in node_properties[node_name]:
                G.get_node_by_id(node_ID).set_label(node_properties[node_name]['label'][1:-1])
            if 'shape' in node_properties[node_name] and 'color' in node_properties[node_name]:
                if node_properties[node_name]['shape'] == 'Mdiamond' and node_properties[node_name]['color'] == 'green':
                    #print("new input :", node_ID)
                    G.add_input_id(node_ID)
                elif node_properties[node_name]['shape'] == 'Msquare' and node_properties[node_name]['color'] == 'red':
                    #print("new output :", node_ID)
                    G.add_output_id(node_ID)

        return G
    
    def is_cyclic(self) -> bool:
        '''
        __________________________
        Return:

        renvoie un boolean qui indique si le graph est cyclique, càd si plusieur node forme une boucle
        __________________________
        '''
        copy = self.copy()
        if len(copy.nodes) == 0:
            return False
        for node in copy.nodes.values():
            if len(node.children) == 0:
                copy.remove_node_by_id(node.id)
                return copy.is_cyclic()
        return True
    
    def min_id(self):
        '''
        __________________________
        Methode:

        renvoie le plus petit ID de node dont le graphe est composé
        __________________________
        '''
        if len(self.nodes) == 0:
            raise ValueError("You are looking for the min of an empty dictionnary")
        cpt = list(self.nodes.keys())[0]
        for node_id in self.nodes.keys():
            if cpt > node_id:
                cpt = node_id
        return cpt
        
    def shift_indice(self,n):
        '''
        __________________________
        Parametre:

        int n: un entier
        __________________________
        Methode:

        Effectue une auglentation de n à chaque ID des nodes du graphe
        __________________________
        '''
        clefs = list(self.nodes.keys())
        newNodes = {}
        newInputs = []
        newOutputs = []
        for i in clefs:
            newParents = {}
            parents = list(self.nodes[i].parents.keys())
            for parentId in parents:
                newParents[parentId+n] = self.nodes[i].parents[parentId]
            self.nodes[i].parents = newParents
            
            newChildren = {}
            children = list(self.nodes[i].children.keys())
            for childrenId in children:
                newChildren[childrenId+n] = self.nodes[i].children[childrenId]
            self.nodes[i].children = newChildren
                
            newNodes[i + n] = self.nodes[i]
            
            self.nodes[i].id += n
        for i in self.inputs:
            newInputs.append(i + n)
        for i in self.outputs:
            newOutputs.append(i + n)
        self.nodes = newNodes
        self.inputs = newInputs
        self.outputs = newOutputs     
        
    def iparallel(self, g):
        '''
        __________________________
        Parametre:

        open_digraph g: un second open digraph
        __________________________
        Methode:

        Ajoute a notre open_digraph un second g sans que ni l'un ni l'autre n'est de lien directe
        __________________________
        '''
        self.shift_indice(g.max_id() - self.min_id() + 1)
        self.nodes.update(g.nodes)
        self.inputs += g.inputs
        self.outputs += g.outputs

    def parallel(self, g):
        '''
        __________________________
        Parametre:

        open_digraph g: un second open_digraph
        __________________________
        renvoie:

        Créer et renvoie un nouveau open_digraph qui contient deux graphe sans que l'un n'est de lien directe avec l'autre
        __________________________
        '''
        newGraph = self.copy()
        newGraph.iparallel(g)
        return newGraph
    
    def icompose(self, g):
        '''
        __________________________
        Parametre:

        open_digraph g: un second open_digraph
        __________________________
        Methode:

        Ajoute a notre open_digraph un second g telque les inputs de notre open_digraph sont relié aux output de g
        __________________________
        '''
        cpt = len(self.inputs)
        if cpt != len(g.outputs) :
            raise ValueError ("You can't merge two digraph, if the inputs of self doesn't match output of g")
        self.iparallel(g)
        for indice in range(cpt):
            self.add_edge(g.outputs[indice], self.inputs[indice])
    
    def compose(self, g):
        '''
        __________________________
        Parametre:

        open_digraph g: un second open_digraph
        __________________________
        Methode:

        Créer et renvoie un nouveau open_digraph qui contient un graphe telque les inputs de notre open_digraph sont relié aux output de g
        __________________________
        '''
        newGraph = self.copy()
        newGraph.icompose(g)
        return newGraph
    
    def connected_components(self):   
        '''
        __________________________
        Return:

        Renvoie tous les graphs parallèle contenue dans un open_digraph avec l'id de 
        __________________________
        '''
        id = 0
        graphs = {}
        for nodeId in self.nodes:
            if not(nodeId in graphs):
                id += 1
                pile = [nodeId]
                while len(pile) > 0:
                    elem = pile.pop()
                    if not(elem in graphs):
                        graphs[elem] = id
                        for parent in self.nodes[elem].parents:
                            if not(parent in graphs):
                                pile.append(parent)
                        for child in self.nodes[elem].children:
                            if not(child in graphs):
                                pile.append(child)
        return id, graphs

    
### TP8 ###

    def fusion_node(self,src : node, tgt : node, name : str = '¤'):
        if not(name == '¤'):
            src.set_label(name)
        for child in tgt.get_children_ids():
            if(child == tgt.get_id()):
                for _ in range(tgt.children[child]):
                    self.add_edge(src.get_id(),src.get_id())
            else :
                for _ in range(tgt.children[child]):
                    self.add_edge(src.get_id(), child)
        for parent in tgt.get_parents_ids():
            if(parent == tgt.get_id()):
                for _ in range(tgt.parents[parent]):
                    self.add_edge(src.get_id(),src.get_id())
            else :
                for _ in range(tgt.parents[parent]):
                    self.add_edge(parent, src.get_id())
        self.remove_node_by_id(tgt.get_id())