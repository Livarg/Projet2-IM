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

if __name__ == '__main__': # the following code is called only when
    unittest.main() # precisely this file is run


