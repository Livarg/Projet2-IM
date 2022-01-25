import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)# allows us to fetch files from the project root
import unittest
from modules.open_digraph import *


class InitTest(unittest.TestCase):
    def test_init_node(self):
        n0 = node(0, 'i', {}, {1:1})
        self.assertEqual(n0.id, 0)
        self.assertEqual(n0.label, 'i')
        self.assertEqual(n0.parents, {})
        self.assertEqual(n0.children, {1:1})
        self.assertIsInstance(n0, node)

    def test_init_open_digraph(self):
        opd = open_digraph([], [], [])
        self.assertEqual(opd.inputs, [])
        self.assertEqual(opd.outputs, [])
        self.assertEqual(opd.nodes, {})
        self.assertIsInstance(opd, open_digraph)
    
    def test_copy(self):
        opd = open_digraph([0], [1], [node(0, "x", {}, {1:1}), node(1, "y", {0:1}, {})])
        self.assertIsNot(opd.copy(),opd)

class NodeTest(unittest.TestCase):
    def setUp(self):
        self.n0 = node(0, 'a', {}, {1:1})

    def test_get_id(self):
        self.assertEqual(self.n0.get_id(), 0)

    def test_get_label(self):
        self.assertEqual(self.n0.get_label(), 'a')
    
    def test_copy(self):
        self.assertIsNot(self.n0.copy(), self.n0)
    
    # TP 2 Exrecice 5
    def test_is_well_formed(self):
        
        n0 = node(0, 'x', {}, {1:1,2:1})
        n1 = node(1, 'y', {0:1}, {2:1})
        n2 = node(2, 'z', {0:1,1:1}, {})
        opd = open_digraph([0],[2],[n0,n1,n2])
        self.assertFalse(opd.is_well_formed())

        n0 = node(0, 'a', {3:1, 4:1}, {1:1, 2:1})
        n1 = node(1, 'b', {0:1}, {2:2, 5:1})
        n2 = node(2, 'c', {0:1, 1:2}, {6:1})
        i0 = node(3, 'i0', {}, {0:1})
        i1 = node(4, 'i1', {}, {0:1})
        o0 = node(5, 'o0', {1:1}, {})
        o1 = node(6, 'o1', {2:1}, {})
        G = open_digraph([3,4], [5,6], [n0,n1,n2,i0,i1,o0,o1])
        self.assert_(G.is_well_formed())



if __name__ == '__main__': # the following code is called only when
    unittest.main() # precisely this file is run


