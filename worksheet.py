from modules.open_digraph import *
from modules.circuit_boolean import *
import inspect

n0 = node(0, 'a', {3:1, 4:1}, {1:1, 2:1})
n1 = node(1, 'b', {0:1}, {2:2, 5:1})
n2 = node(2, 'c', {0:1, 1:2}, {6:1})
i0 = node(3, 'i0', {}, {0:1})
i1 = node(4, 'i1', {}, {0:1})
o0 = node(5, 'o0', {1:1}, {})
o1 = node(6, 'o1', {2:1}, {})
G = open_digraph([3,4], [5,6], [n0,n1,n2,i0,i1,o0,o1])

n3 = node(0, 'x', {}, {1:1,2:1})
n4 = node(1, 'y', {0:1}, {2:1})
n5 = node(2, 'z', {0:1,1:1}, {0:1})

opd = open_digraph([0],[2],[n3,n4,n5])
circuit = bool_circ.random_bool_circ(4,3,3)
circuit_v2 = bool_circ.pars_parenthese("((x0)&(x1)&(x2))|((x1)&(~(x2)))")
G.save_as_dot_file(verbose=True)
#print(opd.is_cyclic())

def print_test():
    print(n0)
    print(n1)
    print(n2)

    print(repr(n0))
    print(repr(n1))
    print(repr(n2))

    print(opd)
    print(repr(opd))

def get_test():
    print(n1.get_id())
    print(n1.get_label())
    print(n1.get_parents_ids())
    print(n1.get_children_ids())

    print(opd.get_input_ids())
    print(opd.get_output_ids())
    print(opd.get_id_node_map())
    print(opd.get_nodes())
    print(opd.get_node_ids())
    print(opd.get_node_by_id(1))
    print(opd.get_nodes_by_ids([1,2]))

def set_test():
    print("node setters")
    n0.set_id(3)
    print(n0.get_id())
    n0.set_label("w")
    print(n0.get_label())
    n0.set_parent_ids({1:2, 2:1})
    print(n0.get_parents_ids())
    n0.set_children_ids({})
    print(n0.get_children_ids())

    n0.add_child_id(4,1)
    print(n0.get_children_ids())
    n0.add_parent_id(0, 0)
    print(n0.get_parents_ids())


    print("\nopen digraph setters")
    opd.set_input_ids([1,2])
    print(opd.get_input_ids())
    opd.set_output_ids([])
    print(opd.get_output_ids())
    opd.add_input_id(1)
    print(opd.get_input_ids())
    opd.add_output_id(4)
    print(opd.get_output_ids())

def exo9():
    print(dir(node))
    print(dir(open_digraph))

    print()

    print(inspect.getsource(node.__init__))
    print(inspect.getdoc(node.__init__))
    print(inspect.getsourcefile(node.__init__))

#Exercice 10
#print(opd.new_id())

def Exercice_11_test():
    print(repr(opd))
    opd.add_edge(2, 0)
    print(repr(opd))
    opd.add_edge(2, 0)
    print(repr(opd))

def Exercice_12_test():
    print(repr(opd))
    opd.add_node('w', {0:2}, {1:1, 2:3})
    print(repr(opd))
    print(opd)

def TP3_ex8_test():
    graph = open_digraph.random_graph(4, 8, 8, 4)
    print(graph)
    print(graph.is_well_formed())

def TP3_ex10_test():
    graph = open_digraph.random_graph(4, 4, 1, 2)
    print(repr(graph))
    print(graph.adjacency_matrix())
    
def TP5_exo_all(opd, G):
    print(G)
    print(opd.min_id(), " ", opd.max_id())
    print(G.min_id(), " ", G.max_id())
    GRAPH = opd.parallel(G)
    print(GRAPH.connected_components())
    
def dijkstra_test(G):
    #On se rend compte que la distance entre i0 et lui même est bien 0
    # la distance entre i0 et o0 est bien 3
    # On voit bien dans prev que b est la node qui précède o0 dans le chemin le plus cours
    dist, prev = G.dijkstra(i0,o0)
    print(dist)
    print("\n", prev)