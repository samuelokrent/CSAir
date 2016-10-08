import json
from graph import Graph

def load(filename, symmetric_routes=True):
    """
    :return: a graph of the json data in the given file
    :param filename: the name of the json file to laod
    :param symmetric_routes: whether the routes in the file should be
        interpreted as symmetric edges
    """
    with open(filename) as data:
        map_data = json.load(data)
        
    nodes = dict()
    for metro in map_data["metros"]:
        nodes[metro["code"]] = metro
    
    g = Graph(nodes)
    
    for route in map_data["routes"]:
        if symmetric_routes:
            g.add_symmetric_edge(route["ports"][0], route["ports"][1], route["distance"])
        else:
            g.add_edge(route["ports"][0], route["ports"][1], route["distance"])
        
    return g

def load_extra(g, filename, symmetric_routes=True):
    """
    adds the data in the given json file the given graph
    :param g: the graph to modify
    :param filename: the name of the json file to load
    :param symmetric_routes: whether the routes in the file should be
        interpreted as symmetric edges
    """
    with open(filename) as data:
        map_data = json.load(data)
        
    for metro in map_data["metros"]:
        g.add_node(metro["code"], metro)
    
    for route in map_data["routes"]:
        if symmetric_routes:
            g.add_symmetric_edge(route["ports"][0], route["ports"][1], route["distance"])
        else:
            g.add_edge(route["ports"][0], route["ports"][1], route["distance"])