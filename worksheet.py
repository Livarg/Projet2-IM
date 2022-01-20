from modules.open_digraph import *

n0 = node(0, 'x', {}, {1:1,2:1})
n1 = node(1, 'y', {0:1}, {2:1})
n2 = node(2, 'z', {0:1,1:1}, {})

opd = open_digraph([0],[2],[n0,n1,n2])

"""
print(n0)
print(n1)
print(n2)

print(repr(n0))
print(repr(n1))
print(repr(n2))

print(opd)
print(repr(opd))
"""
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