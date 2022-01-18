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
        opd = open_digraph([], [], {})
        self.assertEqual(opd.inputs, [])
        self.assertEqual(opd.outputs, [])
        self.assertEqual(opd.nodes, {})
        self.assertIsInstance(opd, open_digraph)

if __name__ == '__main__': # the following code is called only when
    unittest.main() # precisely this file is run


