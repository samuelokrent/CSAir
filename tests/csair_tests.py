import unittest
import graph_parser
from csair_map import Map
import json

class CSAirMapTest(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.airmap = Map("../data/test_data.json")

    def test_city_list(self):
        self.assertEqual(self.airmap.city_list(), [u'Santiago (SCL)', u'Mexico City (MEX)', u'Lima (LIM)'])
        
    def test_city_info(self):
        # full info
        self.assertEqual(self.airmap.city_info('MEX'), {u'code': u'MEX', u'name': u'Mexico City', u'country': u'MX', u'region': 1, u'coordinates': u'19\xb0 N, 99\xb0 W', u'timezone': -6, 'destinations': u'\n\tLima (4231)', u'continent': u'North America', u'population': 23400000})
        # with field supplied
        self.assertEqual(self.airmap.city_info('MEX', 'country'), {'country': u'MX'})
        # incorrect city
        self.assertEqual(self.airmap.city_info('FAKE'), {'ERROR': 'FAKE not a valid code'})
        
    def test_longest_flight(self):
        self.assertEqual(self.airmap.longest_flight(), (u'Mexico City', u'Lima', 4231))
        
    def test_shortest_flight(self):
        self.assertEqual(self.airmap.shortest_flight(), (u'Santiago', u'Lima', 2453))
        
    def test_average_flight(self):
        self.assertEqual(self.airmap.average_flight(), (4231 + 2453) / 2)
        
    def test_biggest_city(self):
        self.assertEqual(self.airmap.biggest_city(), (u'Mexico City', 23400000))
        
    def test_smallest_city(self):
        self.assertEqual(self.airmap.smallest_city(), (u'Santiago', 6000000))
        
    def test_average_population(self):
        self.assertEqual(self.airmap.average_population(), (9050000 + 23400000 + 6000000) / 3)
        
    def test_continent_list(self):
        self.assertEqual(self.airmap.continent_list(), u'North America: \n\tMexico City\nSouth America: \n\tSantiago\n\tLima')

    def test_hubs(self):
        # up to 10
        self.assertEqual(self.airmap.hubs(), [(u'Lima', 2), (u'Mexico City', 1), (u'Santiago', 1)])
        # limit of 1
        self.assertEqual(self.airmap.hubs(1), [(u'Lima', 2)])
    
    def test_visualizer_url(self):
        self.assertEqual(self.airmap.visualizer_url(), 'http://www.gcmap.com/mapui?P=SCL-LIM,MEX-LIM,LIM-SCL,LIM-MEX')
        
    def test_remove_city(self):
        self.assertTrue("SCL" in self.airmap.graph)
        self.assertEqual(self.airmap.remove_city("SCL"), 'Removed SCL')
        self.assertFalse("SCL" in self.airmap.graph)
        
    def test_add_city(self):
        city_json = json.dumps({
            "code": "AAA",
            "name": "AAA",
            "country": "AAA",
            "continent": "AAA",
            "timezone": +5,
            "coordinates": {"S": 1, "W": 1},
            "population": 500,
            "region": "AAA"
            })
        self.assertEqual(self.airmap.add_city("AAA", city_json), "Added AAA")
        self.assertTrue("AAA" in self.airmap.graph)
        
        city_json = json.dumps({
            "code": "BBB"
            })
        self.assertEqual(self.airmap.add_city("BBB", city_json), "Missing field: name")
        self.assertFalse("BBB" in self.airmap.graph)
        
    def test_remove_route(self):
        self.assertEqual(self.airmap.remove_route("FAKE", "BLAH"), 'Error: could not remove FAKE-BLAH')
        
        self.assertTrue(self.airmap.graph.is_edge_between("MEX", "LIM"))
        self.assertEqual(self.airmap.remove_route("MEX", "LIM"), 'Removed MEX-LIM')
        self.assertFalse(self.airmap.graph.is_edge_between("MEX", "LIM"))
        
    def test_add_route(self):
        self.assertFalse(self.airmap.graph.is_edge_between("MEX", "SCL"))
        self.assertEqual(self.airmap.add_route("MEX", "SCL", 100), 'Added MEX-SCL')
        self.assertTrue(self.airmap.graph.is_edge_between("MEX", "SCL"))
        self.assertEqual(self.airmap.graph.distance_between("MEX", "SCL"), 100)
        
    def test_route_info(self):
        self.assertEqual(self.airmap.route_info(["MEX", "LIM", "SCL"]), '======== Route info ========\nTotal distance: 6684 km\nTotal cost: $2216.75\nTotal time: 11.81 hours\n')
        
    def test_shortest_path(self):
        self.assertEqual(self.airmap.shortest_path("MEX", "SCL"), 'Shortest route: MEX-LIM-SCL\n\n======== Route info ========\nTotal distance: 6684 km\nTotal cost: $2216.75\nTotal time: 11.81 hours\n')

if __name__ == '__main__':
    unittest.main()