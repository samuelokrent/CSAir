import unittest
from graph import Graph
from graph import Node
import graph_parser

class GraphTest(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        g = Graph({"A": 1, "B": 2, "C": 3, "D": 4, "E": 5})
        g.add_edge("A", "B", 4)
        g.add_edge("A", "C", 2)
        g.add_edge("C", "B", 1)
        g.add_edge("B", "D", 3)
        g.add_edge("C", "D", 6)
        g.add_edge("B", "E", 1)
        g.add_edge("C", "E", 5)
        g.add_edge("E", "D", 7)
        self.big_graph = g

    def test_basic_graph(self):
        g = Graph({"A": 1, "B": 2})
        self.assertEqual(len(g.nodes), 2)
        self.assertEqual(len(g.edges), 2)
        self.assertEqual(len(g.edges["A"]), 2)
        self.assertIsNone(g.edge("A", "B"))
        self.assertTrue(0 <= g.node_index("A") and g.node_index("A") < 2)
        self.assertEqual(set(g.node_ids()), set(["A", "B"]))
        self.assertEqual(g.node("B"), Node("B", 2))
        
    def test_graph_with_edges(self):
        g = Graph({"A": 1, "B": 2, "C": 3})
        g.add_edge("A", "B", 5)
        self.assertEqual(g.distance_between("A", "B"), 5)
        self.assertEqual(g.distance_between("C", "B"), float("inf"))
        
        g.add_symmetric_edge("C", "A", 8)
        self.assertEqual(len(g.children("A")), 2)
        self.assertEqual(len(g.children("C")), 1)
        self.assertEqual(len(g.children("B")), 0)
        self.assert_(g.is_edge_between("A", "C"))
        
        g.remove_edge("A", "C")
        self.assertEqual(len(g.children("A")), 1)
        self.assertEqual(len(g.children("C")), 1)
        self.assertFalse(g.is_edge_between("A", "C"))
        
    def test_remove_node(self):
        g = self.big_graph
        self.assertTrue("A" in g)
        g.remove_node("A")
        self.assertFalse("A" in g)
        
    def test_out_deg(self):
        g = self.big_graph
        self.assertEqual(g.out_deg("A"), 2)
        self.assertEqual(g.out_deg("C"), 3)
        self.assertEqual(g.out_deg("D"), 0)
        
    def test_path_length(self):
        g = self.big_graph
        self.assertEqual(g.path_length(["A", "B", "D"]), 7)
        self.assertEqual(g.path_length(["D"]), 0)
        self.assertEqual(g.path_length(["A", "C", "E", "D"]), 14)
        
    def test_dijkstras(self):
        g = self.big_graph
        self.assertEqual(g.dijkstras("A", "E"), ["A", "C", "B", "E"])
        
        g.remove_edge("C", "B")
        self.assertEqual(g.dijkstras("A", "E"), ["A", "B", "E"])
        
        g.add_edge("A", "E", 3)
        self.assertEqual(g.dijkstras("A", "E"), ["A", "E"])
        
        # test from node to itself
        self.assertEqual(g.dijkstras("E", "E"), ["E"])
        
        # test when path does not exist
        self.assertIsNone(g.dijkstras("D", "A"))
        
class ParserTest(unittest.TestCase):
        
        def test_load_data(self):
            g = graph_parser.load("../data/test_data.json")
            self.assertEqual(set(g.node_ids()), set(["SCL", "MEX", "LIM"]))
            
            self.assertEqual(len(g.children("LIM")), 2)
            self.assertEqual(len(g.children("SCL")), 1)
            self.assertEqual(len(g.children("MEX")), 1)
            
            self.assertIn(Node("SCL", None), g.children("LIM"))
            self.assertIn(Node("LIM", None), g.children("SCL"))
            self.assertIn(Node("MEX", None), g.children("LIM"))
            self.assertIn(Node("LIM", None), g.children("MEX"))
            
            self.assert_(g.is_edge_between("LIM", "MEX"))
            self.assert_(g.is_edge_between("MEX", "LIM"))
            self.assert_(g.is_edge_between("LIM", "SCL"))
            self.assert_(g.is_edge_between("SCL", "LIM"))
            self.assertFalse(g.is_edge_between("MEX", "SCL"))
            self.assertFalse(g.is_edge_between("SCL", "MEX"))
            
            self.assertEqual(g.distance_between("LIM", "MEX"), 4231)
            self.assertEqual(g.distance_between("MEX", "LIM"), 4231)
            self.assertEqual(g.distance_between("LIM", "SCL"), 2453)
            self.assertEqual(g.distance_between("SCL", "LIM"), 2453)
            self.assertEqual(g.distance_between("MEX", "SCL"), float("inf"))
            self.assertEqual(g.distance_between("SCL", "MEX"), float("inf"))
            
            self.assertEqual(g.node("LIM").data["name"], "Lima")
            self.assertEqual(g.node("MEX").data["name"], "Mexico City")
            self.assertEqual(g.node("SCL").data["name"], "Santiago")
            

if __name__ == '__main__':
    unittest.main()