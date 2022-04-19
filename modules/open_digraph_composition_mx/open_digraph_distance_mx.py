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


class open_digraph_distance_mx:
    def dijkstra(self, src : node, tgt : node = None, direction = None):
        '''
        __________________________
        Parametre:

        node src : node de la quelle on part 
        node tgt : node jusqu'à la qu'elle on va. Si none on va jusqu'au bout du graph
        direction : -1,1,none indique si l'on cherche la node tgt dans les enfants, les parents ou les deux
        __________________________
        Return:

        dict node, int dist  : un dictionnaire qui associe chaque node à la distance minimale de src,
                               peux ne pas etre complet si tgt est specifie et est atteint avant d'etre passe sur toutes les nodes
        dict node, node prev : un dictionnaire qui associe une node a une autre voisine tel que dist[node] = dist[voisine] + 1
                               suivre cette chaine de voisinne cree le chemin le plus court de node a src,
                               peux ne pas etre complet si tgt est specifie et est atteint avant d'etre passe sur toutes les nodes
        __________________________
        '''
        Q = [src]
        dist = {src : 0}
        prev = {}
        while(len(Q) != 0):
            u = Q.pop(0)  #Pas besoin de récupérer le min de dist car nos list car Q est déjà sensé etre trié dans l'ordre croissant (création de Q)
            if(direction == -1):
                neighbours = self.get_nodes_by_ids(list(u.get_parents_ids()))
            elif(direction == 1):
                neighbours = self.get_nodes_by_ids(list(u.get_children_ids()))
            else:
                neighbours = self.get_nodes_by_ids(list(u.get_parents_ids()) + list(u.get_children_ids()))
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
        renvoie res une liste de tuple de node telque le rang dans cette liste indique le nombre parents qu'à la node soit sa profondeur
        
        renvoie une erreure si le graph est cyclique (Si il existe un groupe de node telle que toute nodes aient un parent)
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
    