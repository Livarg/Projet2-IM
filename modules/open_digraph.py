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


class open_digraph(node): # for open directed graph
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

    def copy(self):
        '''
        __________________________
        Methode:

        Créer une coupie d'un graphe, la copie et l'original sont bien 2 instances différentes
        __________________________
        '''
        nodes = []
        for node in self.nodes.values():
            nodes.append(node)
        _copy = open_digraph(self.inputs.copy(), self.outputs.copy(), nodes)
        return _copy

    @classmethod
    def empty(self):
        return open_digraph([],[],[])


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

    @classmethod
    def graph_from_adjacency_matrix(self, matrix: List[List[int]]):
        graph = self.empty()
        for i in range(len(matrix)):
            graph.add_node(str(i))
        for x in range(len(matrix)):
            for y in range(len(matrix)):
                for _ in range(matrix[x][y]):
                    graph.add_edge(x,y)
        return graph

    @classmethod
    def random(self, n: int, bound: int, inputs: int = 0, outputs: int = 0, form: str = "free"):
        '''
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
        Method:

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
        Method:

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
        file = open(path + "/Open_digraph.dot", "w+")
        file.writelines("digraph G { \n\n")
        for node in self.nodes.values() :
            for ID in node.children :
                for _ in range(node.children[ID]) : 
                    file.write("    " + str(node.get_id()) + "->" + str(self.nodes[ID].get_id()) + ";\n")
            if verbose :
                file.write("    " + str(node.get_id()) + "[label = " + node.get_label()  + "_" + str(node.get_id())+ "]; \n" )
            if node.get_id() in self.get_input_ids():
                file.write("    " + str(node.get_id()) + "[shape = Mdiamond, color = green];\n")
            if node.get_id() in self.get_output_ids():
                file.write("    " + str(node.get_id()) + "[shape = Msquare, color = red];\n")
        file.write("\n}")
        file.close()

    '''def from_dot_file(file):
    #J'ai chié ça avec trop de fatigue pour que ce soit clair et j'ai eu la flemme de le tester : 
    #i.e. c'est sur que ca marche pas deso (mais je peux le reexpliquer si besoin ptdr)
    
        File = open(file, "r")
        file = File.read()
        node_list = []
        for line in file:
            line = line.replace("    ","")
            i = 0
            n = ""
            while line[i] != "-":
                n += line[i]
                i+=1
            n_id = int(n)
                
            line = line.replace("->","")
            i-=1
            n_child = []
            while line[i] != ";" : 
                n_child.append(stoi(line[i]))
                i+=1

            n_label = n
            if "label" in line[i+1]:
                j=0
                line = line.replace("    ","")
                line = line.replace("[label= ")
                line = line.replace("]")
                while line[j]!=" ":
                    n_label += line[j]

            n_parent = [] 
            if len(node_list)>0 :
                for k in range(len(node_list)) :
                    for l in range(len(node_list[k])):
                        if node_list[k][l] == n_id :
                            n_parent.append(node_list[k][0])
                
            node_list.append( node(n_id,n_label,n_parent,n_child) )
            
            inputs = []
            outputs = []
            #pour la suite on suppose qu'il y a forcement le label (pas trouvé comment faire autrement)
            for index in range(len(node_list)) :
                if "o" in node_list[index][1] :
                    outputs.append(node_list[index][0])
                    node_list.del(node_list[index])
                elif "i" in node_list[index][1] : 
                    inputs.append(node_list[index][0])
                    node_list.del(node_list[index])
            return open_digraph(inputs,outputs,node_list)'''
    
    def is_cyclic(self) -> bool:
        copy = self.copy()
        if len(copy.nodes) == 0:
            return False
        for node in copy.nodes.values():
            if len(node.children) == 0:
                copy.remove_node_by_id(node.id)
                return copy.is_cyclic()
        return True
    
    def min_id(self):
        if len(self.nodes) == 0:
            raise ValueError("You are looking for the min of an empty dictionnary")
        cpt = list(self.nodes.keys())[0]
        for node_id in self.nodes.keys():
            if cpt > node_id:
                cpt = node_id
        return cpt
    
    def max_id(self):
        if len(self.nodes) == 0:
            raise ValueError("You are looking for the max of an empty dictionnary")
        cpt = list(self.nodes.keys())[0]
        for node_id in self.nodes.keys():
            if cpt < node_id:
                cpt = node_id
        return cpt
        
    def shift_indice(self,n):
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
        self.shift_indice(g.max_id() - self.min_id() + 1)
        self.nodes.update(g.nodes)
        self.inputs += g.inputs
        self.outputs += g.outputs

    def parallel(self, g):
        newGraph = self.copy()
        newGraph.iparallel(g)
        return newGraph
    
    def icompose(self, g):
        cpt = len(self.inputs)
        if cpt != len(g.outputs) :
            raise ValueError ("You can't merge two digraph, if the inputs of self doesn't match output of g")
        self.iparallel(g)
        for indice in range(cpt):
            self.add_edge(g.outputs[indice], self.inputs[indice])
        
    
    def compose(self, g):
        newGraph = self.copy()
        newGraph.icompose(g)
        return newGraph
    
    def connected_components(self):
        
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

    def dijkstra(self, src : node, tgt : node = None, direction = None):
        Q = [src]
        dist = {src : 0}
        prev = {}
        while(len(Q) != 0):
            u = Q.pop(0).get_id()  #Pas besoin de récupérer le min de dist car nos list car Q est déjà sensé etre trié dans l'ordre croissant (création de Q)
            if(direction == -1):
                neighbours = self.get_node_by_ids(list(u.get_parents_ids()))
            elif(direction == 1):
                neighbours = self.get_node_by_ids(list(u.get_childrens_ids()))
            else:
                neighbours = self.get_node_by_ids(list(u.get_parents_ids()) + list(u.get_childrens_ids()))
            for v in neighbours:
                if not(v in dist):
                    Q.append(v)
                if not(v in dist) or dist[v] > dist[u] + 1:
                    dist[v] = dist[u] + 1
                    prev[v] = u
                if v == tgt:
                    return dist, prev
        return dist, prev
            
    def shortest_path(self, u : node, v : node, direction = 1):
        dist, prev = self.dijkstra(u , v, direction)
        if not(v in dist):
            raise ValueError("Il n'existe pas de chemin de u à v :(")
        res = [v]
        while(v in prev):
            res.append(prev[v])
            v = prev[v]
        return res.reverse()

    def common_ancestor_distances(self, u: node, v : node):
        ancestor_u = self.get_nodes_by_ids(list(u.get_parents_ids()))
        ancestor_v = self.get_nodes_by_ids(list(v.get_parents_ids()))
        
        for node in ancestor_u:
            ancestor_u.append(self.get_nodes_by_ids(list(node.get_parents_ids())))
        for node in ancestor_v:
            ancestor_v.append(self.get_nodes_by_ids(list(node.get_parents_ids())))
        
        ancestor = [node for node in ancestor_u if node in ancestor_v]
        dist = {}
        
        for node in ancestor:
            dist[node.get_id()] = self.shortest_path(node , u), self.shortest_path(node , v)
        
        return dist
    
    def tri_topologique(self):
        res = []
        copy = self.copy()
        copy.remove_nodes_by_id(copy.get_input_ids())
        copy.remove_nodes_by_id(copy.get_output_ids())
        while (len(copy.get_nodes()) > 0):
            top = [node.get_id() for node in copy.get_nodes() if len(node.get_parents_ids()) == 0]
            if(len(top) == 0):
                raise ValueError("Le graphe est cyclique.")
            res.append(top)
            copy.remove_nodes_by_id(top)
        return res
    
    def depth_node(self, u : node):
        tri = self.tri_topologique()
        for index, nodes in enumerate(tri):
            if u.get_id() in nodes:
                return index
            
    def depth(self):
        return len(self.tri_topologique())
    
    def longest_path(self, u: node, v: node):
        tri = self.tri_topologique()
        k = 0
        while u.get_id() not in tri[k]:
            k += 1
        
        dist = {u : 0}
        prev = {}
        while v.get_id() not in tri[k]:
            for wID in tri[k]:
                w = self.get_node_by_id(wID)
                for parentID in w.get_parents_ids():
                    parent = self.get_node_by_id(parentID)
                    if parent in dist:
                        if w not in dist or dist[parent] >= dist[w]:
                            dist[w] = dist[parent] + 1
                            prev[w] = parent
            k += 1
        for parentID in v.get_parents_ids():
            parent = self.get_node_by_id(parentID)
            if parent in dist:
                if v not in dist or dist[parent] >= dist[w]:
                    dist[w] = dist[parent] + 1
                    prev[w] = parent
        
        if not(v in dist):
            raise ValueError("Il n'existe pas de chemin de u à v :(")
        res = [v]
        while(v in prev):
            res.append(prev[v])
            v = prev[v]
        return res.reverse(), len(res)
                            


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