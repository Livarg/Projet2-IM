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


class open_digraph(open_digraph_base_mx, open_digraph_methode_mx): # for open directed graph
    def copy(self):
        '''
        __________________________
        Methode:

        Créer une copie d'un graphe, la copie et l'original sont bien 2 instances différentes
        __________________________
        '''
        nodes = []
        for node in self.nodes.values():
            nodes.append(node)
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
            graph.add_node(str(i))
        for x in range(len(matrix)):
            for y in range(len(matrix)):
                for _ in range(matrix[x][y]):
                    graph.add_edge(x,y)
        return graph

    @classmethod
    def random(self, n: int, bound: int, inputs: int = 0, outputs: int = 0, form: str = "free"):
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



    def dijkstra(self, src : node, tgt : node = None, direction = None):
        '''
        __________________________
        Parametre:

        node src : node de la quelle on part 
        node tgt : node jusqu'à la qu'elle on va. Si none on va jusqu'au bout du graph
        direction : -1,1,none indique si l'on cherche la node tgt dans les enfants, les parents ou les deux
        __________________________
        Return:

        dist Calcul la distance entre 2 node, c'est à dire le nombre de noeud minimal plus 1
        prev : un dictionnaire contenant les ID des nodes sur les qu'elles on est passé
        __________________________
        '''
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
        '''
        __________________________
        Parametre:

        node u: une node quelconque
        node v; une node quelconque
        __________________________
        Return:

        Renvoie un dictionnaire contenant le chemin le plus entre les nodes u et v
        __________________________
        '''
        dist, prev = self.dijkstra(u , v, direction)
        if not(v in dist):
            raise ValueError("Il n'existe pas de chemin de u à v :(")
        res = [v]
        while(v in prev):
            res.append(prev[v])
            v = prev[v]
        return res.reverse()

    def common_ancestor_distances(self, u: node, v : node):
        '''
        __________________________
        Parametre:

        node u: une node quelconque
        node v; une node quelconque
        __________________________
        Return:

        dictionnaire dist : un dictionnaire contenant pour clé l'ID d'une node parent de u et v et pour valeur le tuple de la distance a u puis v
        __________________________
        '''
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
        '''
        __________________________
        Return:

        res list : une liste de tuple de node
        renvoie res une liste de tuple de node telque le rang dans cette liste indique le nombre parents qu'à la node
        
        renvoie une erreure si le graph est cyclique (Si il existe un groupe de node telque toute ai un parent)
        __________________________
        '''
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
        '''
        __________________________
        Return:

        Renvoie la profondeur d'un graph c'est a dire le nombre maximal de parent que possède une node
        __________________________
        '''
        return len(self.tri_topologique())
    
    def longest_path(self, u: node, v: node):
        '''
        __________________________
        Parametre:

        node u: une node quelconque
        node v; une node quelconque
        __________________________
        Return:

        res list : une list de node contenant le chemin entre u et v
        len(res) entier : le nombre de node entre qui sépare au macimum u et v
        
        Renvoie le chemin avec la plus grande distance possible entre deux nodes dans un graph acyclique ainsi que la distance parcourue
        __________________________
        '''
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