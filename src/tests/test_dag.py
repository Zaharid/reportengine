# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 15:01:41 2015

@author: zah
"""


import unittest

from dag import DAG, CycleError

class TestDAG(unittest.TestCase):
    
    @staticmethod
    def make_diamond():
        g = DAG()
        g.add_node(0)
        g.add_node(1, inputs={0})
        g.add_node(2, inputs={0})
        g.add_node(3, inputs={1,2})
        
        return g
    
    def make_graphs(self):
        return [self.make_diamond()]
    
    def test_add(self):
        g = DAG()
        g.add_node(1)
        g.add_node(2)
        g.add_node(3, inputs = {1,2})
        g.add_node(0, outputs={1})
        self.assertEqual(g._head_nodes, g.to_nodes({0,2}))
        self.assertEqual(g._leaf_nodes, g.to_nodes({3}))
    
    def test_inter(self):
        for g in self.make_graphs():
            self.assertEqual(len(set(g)), len(list(g)))

    def test_diamond(self):
        
        g = self.make_diamond()
        first_child = {o for node in g._head_nodes for o in node.outputs}
        self.assertEqual(first_child, g.to_nodes({1,2}))

        nodes = list(g.topological_iter())
        self.assertEqual({nodes[0]}, g.to_nodes({0}))
        self.assertEqual(set(nodes[1:3]), g.to_nodes({1,2}))
        self.assertEqual({nodes[3]}, g.to_nodes({3}))
        
        nodes = list(g.breadthfirst_iter())
        self.assertEqual({nodes[0]}, g.to_nodes({0}))
        self.assertEqual(set(nodes[1:3]), g.to_nodes({1,2}))
        self.assertEqual({nodes[3]}, g.to_nodes({3}))
        
        nodes = list(g.deepfirst_iter())
        self.assertEqual({nodes[0]}, g.to_nodes({0}))
        self.assertEqual({nodes[2]}, g.to_nodes({3}))
    
    def test_cycles(self):
        g = self.make_diamond()
        refs =g._node_refs.copy()
        with self.assertRaises(CycleError):
            g.add_node(5, inputs={3}, outputs={0})
        self.assertNotIn(5, g)
        self.assertEqual(refs, g._node_refs)
    
    def test_dependency_resolver(self):
        g = self.make_diamond()
        resolver = g.dependency_resolver()
        self.assertEqual(resolver.send(None), {0})
        self.assertEqual(resolver.send(0), {1,2})
        self.assertEqual(resolver.send(1), set())
        self.assertEqual(resolver.send(2), {3})
        
        resolver = g.dependency_resolver()
        resolver.send(None)
        resolver.send(0)
        resolver.send(1)
        with self.assertRaises(ValueError):
            resolver.send(1)

if __name__ == "__main__":
    unittest.main()