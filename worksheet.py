from modules.open_digraph import *

n0 = node(0, 'x', {}, {1:1,2:1})
n1 = node(1, 'y', {0:1}, {2:1})
n2 = node(2, 'z', {0:1,1:1}, {})

opd = open_digraph([0],[2],[n0,n1,n2])

print(n0)
print(n1)
print(n2)

print(repr(n0))
print(repr(n1))
print(repr(n2))

print(opd)
print(repr(opd))