from modules.open_digraph import *
import inspect

n0 = node(0, 'x', {}, {1:1,2:1})
n1 = node(1, 'y', {0:1}, {2:1})
n2 = node(2, 'z', {0:1,1:1}, {})

opd = open_digraph([0],[2],[n0,n1,n2])

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

Exercice_12_test()