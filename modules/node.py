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


class node:
    def __init__(self, identity: int, label: str, parents: Dict[int, int], children: Dict[int, int]) -> None:
        '''
        __________________________
        Attribut:

        identity: int; its unique id in the graph
        label: string;
        parents: int->int Dict; maps a parent node's id to its multiplicity
        children: int->int Dict; maps a child node's id to its multiplicity
        __________________________
        '''
        self.id = identity
        self.label = label
        self.parents = parents
        self.children = children

    def __str__(self) -> str:
        parents = "[ "
        children = "[ "
        for parentID in self.parents:
            parents += f'{parentID}, '
        parents += "]"
        for childrenID in self.children:
            children += f'{childrenID}, '
        children += "]"
        res = f"Name : {self.label}; ID = {self.id}; Parents : {parents}; Children : {children}"
        return res
    
    def __repr__(self) -> str:
        return f'node({self.id}, "{self.label}", {self.parents}, {self.children})'
    
    def copy(self):
        '''
        __________________________
        Methode : Créer une copie d'une node
        __________________________
        '''
        copyParents = {nodeID:self.parents[nodeID] for nodeID in self.parents}
        copyChildren = {nodeID:self.children[nodeID] for nodeID in self.children}
        _copy = node(self.id, self.label, copyParents, copyChildren)
        return _copy
    
    #getters
    def get_id(self) -> int:
        return self.id
    
    def get_label(self) -> str:
        return self.label
    
    def get_parents_ids(self) -> List[int]:
        return list(self.parents.keys())
    
    def get_children_ids(self) -> List[int]:
        return list(self.children.keys())
    
    #setters
    def set_id(self, id: int) -> None:
        '''
        __________________________
        Parametre:
        
        id: int; the new id of the node
        __________________________
        '''
        self.id = id
    
    def set_label(self, label: str) -> None:
        '''
        __________________________
        Parametre:

        label: string; the new label of the node
        __________________________
        '''
        self.label = label
    
    def set_parent_ids(self, parent_ids: Dict[int, int]) -> None:
        '''
        __________________________
        Parametre:

        parent_ids: int->int Dict; the new parents of the node
        __________________________
        '''
        self.parents = parent_ids
    
    def set_children_ids(self, children_ids: Dict[int, int]) -> None:
        '''
        __________________________
        Parametre:

        children_ids: int->int Dict; the new children of the node
        __________________________
        '''
        self.children = children_ids
    
    def add_child_id(self, child_id: int, mult: int) -> None:
        '''
        __________________________
        Parametre:
        
        child_id: int; the id of the new child of the node
        mult: int; the multiplicity of the child
        __________________________
        Methode:

        __________________________
        '''
        if not(child_id in self.children):
            self.children[child_id] = mult
    
    def add_parent_id(self, parent_id: int, mult: int) -> None:
        '''
        __________________________
        Parametre:

        parent_id: int; the id of the new parent of the node
        mult: int; the multiplicity of the parent
        __________________________
        Methode:

        __________________________
        '''
        if not(parent_id in self.parents):
            self.parents[parent_id] = mult

    def remove_parent_once(self, parent_id: int) -> None:
        '''
        __________________________
        Parametre:

        parent_id : int; le numéro d'identification d'une node
        __________________________
        Methode:
        Vérifie que l'id rentré appartient au node parent de la node actuelle
        Si oui retire un lien entre les nodes
        Si non raise une ereure
        __________________________
        '''
        if not(parent_id in self.parents):
            raise ValueError("Le parents n'existe pas!")
        else :
            self.parents[parent_id] -= 1
        if (self.parents[parent_id] == 0):
            self.parents.pop(parent_id)

    def remove_parent_id(self, parent_id: int) -> None:
        '''
        __________________________
        Parametre:

        parent_id : int; le numéro d'identification d'une node
        __________________________
        Methode:

        Vérifie que l'id rentré appartient au node parent de la node actuelle
        Si oui retire tous les liens entre les nodes
        Si non raise une erreure
        __________________________
        '''
        if not(parent_id in self.parents):
            raise ValueError("Le parents n'existe pas!")
        else:
            self.parents.pop(parent_id)

    def remove_child_once(self, child_id: int):
        '''
        __________________________
        Parametre:

        child_id : int; le numéro d'identification d'une node
        __________________________
        Methode:

        Vérifie que l'id rentré appartient au node enfant de la node actuelle
        Si oui retire un liens entre les nodes
        Si non raise une erreure (l'enfant n'existe pas)
        __________________________
        '''
        if not(child_id in self.children):
            raise ValueError("L'enfant n'existe pas!")
        else :
            self.children[child_id] -= 1
        if (self.children[child_id] == 0):
            self.children.pop(child_id)

    def remove_child_id(self, child_id: int) -> None:
        '''
        __________________________
        Parametre:

        child_id : int; le numéro d'identification d'une node
        __________________________
        Methode:

        Vérifie que l'id rentré appartient au node enfant de la node actuelle
        Si oui retire tous liens entre les nodes
        Si non raise une erreure (l'enfant n'existe pas)
        __________________________
        '''
        if not(child_id in self.children):
            raise ValueError("L'enfant n'existe pas!")
        else :
            self.children.pop(child_id)
    
    def indegree(self) -> int:
        sum = 0
        for parent in self.parents.values():
            sum += parent
        return sum

    def outdegree(self) -> int:
        sum = 0
        for child in self.children.values():
            sum += child
        return sum

    def degree(self) -> int:
        return self.outdegree() + self.indegree()
        
