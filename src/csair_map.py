from graph import Graph
from graph import Node
import graph_parser
import heapq
import json
from math import sqrt
from fileinput import filename

class Map:
    """
    Map: A wrapper for the Graph class that includes
    CSAir-specific functionality
    """
    
    
    # constants pertaining to plane travel
    PRICE_PER_KM = 0.35
    CONNECTING_DISCOUNT = 0.05
    
    PLANE_SPEED = 750.0
    ACCELERATION_DISTANCE = 200.0
    ACCELERATION_TIME = 2 * ACCELERATION_DISTANCE / PLANE_SPEED
    PLANE_ACCELERATION = (PLANE_SPEED) / ACCELERATION_TIME
    
    
    def __init__(self, data_file, symmetric_routes=True):
        """
        creates a new CSAir Map from the given json file
        :param data_file: the name of the json file to laod
        :param symmetric_routes: whether the routes in the file
            should be interpreted as symmetric edges
        """
        self.graph = graph_parser.load(data_file, symmetric_routes=symmetric_routes)
        try:
            with open(data_file) as data:
                self.data_sources = json.load(data)["data sources"]
        except:
            self.data_sources = []
        
    def city_list(self):
        """
        :return: a list of the names of all cities in the map
        """
        return [node.data["name"] + (" (%s)" % node.data["code"]) for node in self.graph.nodes]
    
    # returns a dictionary of information on the city whose code is supplied
    # code: the code of the city
    # field: the name of the field to narrow the info down to
    def city_info(self, code, field=None):
        """
        :return: a dictionary of information on the city whose code is supplied
        :param code: the code of the city
        :param field: the name of the field to narrow the info down to
        """
        try:
            info = self.graph.node(code).data.copy()
        except:
            return { "ERROR": "%s not a valid code" % code }
         
        coords = info["coordinates"]
        coord_string = ""
        try:
            coord_string += "%s%s N" % (coords["N"], u'\xb0')
        except:
            coord_string += "%s%s S" % (coords["S"], u'\xb0')
        try:
            coord_string += ", %s%s E" % (coords["E"], u'\xb0')
        except:
            coord_string += ", %s%s W" % (coords["W"], u'\xb0')
        info["coordinates"] = coord_string
        
        dests = ["%s (%s)" % (node.data["name"], self.graph.distance_between(code, node.data["code"])) for node in self.graph.children(code)]
        info["destinations"] = "\n\t" + "\n\t".join(dests)
        
        if field != None:
            try:
                return { field: info[field] }
            except:
                return { "ERROR": "%s not a valid field" % field }
        else:
            return info
        
    
    def longest_flight(self):
        """
        :return:a tuple of the src city, dst city, and length
            of the longest flight in the map
        """
        max_dist = -1
        cities = ["", ""]
        for c1 in self.graph.edges:
            for c2 in self.graph.edges[c1]:
                dist = self.graph.edges[c1][c2]
                if dist != None and dist > max_dist:
                    max_dist = dist
                    cities = [self.graph.node(c1).data["name"], self.graph.node(c2).data["name"]]
        return (cities[0], cities[1], max_dist)
    
    def shortest_flight(self):
        """
        :return:a tuple of the src city, dst city, and length
            of the shortest flight in the map
        """
        min_dist = float("inf")
        cities = ["", ""]
        for c1 in self.graph.edges:
            for c2 in self.graph.edges[c1]:
                dist = self.graph.edges[c1][c2]
                if dist != None and dist < min_dist:
                    min_dist = dist
                    cities = [self.graph.node(c1).data["name"], self.graph.node(c2).data["name"]]
        return (cities[0], cities[1], min_dist)
    
    def average_flight(self):
        """
        :return: the average distance of all flights in the map
        """
        sum = 0
        count = 0
        for c1 in self.graph.edges:
            for c2 in self.graph.edges[c1]:
                dist = self.graph.edges[c1][c2]
                if dist != None:
                    sum += dist
                    count += 1
        return sum / count
    
    def biggest_city(self):
        """
        :return: a tuple of the name and population of
        the largest city in the map
        """
        max_pop = -1
        city = ""
        for node in self.graph.nodes:
                pop = node.data["population"]
                if pop > max_pop:
                    max_pop = pop
                    city = node.data["name"]
        return (city, max_pop)
    
    def smallest_city(self):
        """
        :return: a tuple of the name and population of
        the smallest city in the map
        """
        min_pop = float("inf")
        city = ""
        for node in self.graph.nodes:
                pop = node.data["population"]
                if pop < min_pop:
                    min_pop = pop
                    city = node.data["name"]
        return (city, min_pop)
    
    def average_population(self):
        """
        :return: the average population of all cities in the map
        """
        sum = 0
        count = 0
        for node in self.graph.nodes:
                sum += node.data["population"]
                count += 1
        return sum / count
    
    def continent_list(self):
        """
        :return: a string list of all continents in the map,
            and the cities that lie within them
        """
        cities = dict()
        for node in self.graph.nodes:
            if not cities.has_key(node.data["continent"]):
                cities[node.data["continent"]] = list()
            cities[node.data["continent"]].append(node.data["name"])
        for continent in cities:
            cities[continent] = "\n\t" + "\n\t".join(cities[continent])
        return "\n".join(["%s: %s" % (continent, cities[continent]) for continent in cities])
    
    def hubs(self, num=10):
        """
        :return: a list of num hub cities
        each city is represented as a tuple of (name, # of direct connections)
        """
        hubs = []
        for node in self.graph.nodes:
            flight_count = sum([self.graph.edges[node.nid][dest] != None for dest in self.graph.edges[node.nid]])
            # minheap sorts in ascending order, so negate flight_count
            heapq.heappush(hubs, (-flight_count, node.data["name"]))
        return [(pair[1], -pair[0]) for pair in [heapq.heappop(hubs) for i in range(min(num, len(hubs)))]]
    
    def visualizer_url(self):
        """
        :return: the url of the gcmap.com map that visualizes the map data
        """
        url = "http://www.gcmap.com/mapui?P="
        routes = []
        for c1 in self.graph.node_ids():
            for c2 in self.graph.node_ids():
                if self.graph.is_edge_between(c1, c2):
                    routes.append("%s-%s" % (c1, c2))
        return url + ",".join(routes)
    
    def remove_city(self, code):
        """
        removes the city of the given code from the map
        """
        try:
            self.graph.remove_node(code)
            return "Removed %s" % code
        except:
            return "Error: could not remove %s" % code
        
    def add_city(self, nid, data):
        """
        adds the given city to the map
        """
        try:
            parsed_data = json.loads(data)
        except:
            return "Error: could not parse JSON data"
        
        for field in [
            "code",
            "name",
            "country",
            "continent",
            "timezone",
            "coordinates",
            "population",
            "region"
        ]:
            if field not in parsed_data:
                return "Missing field: %s" % field
            
        self.graph.add_node(nid, data)
        return "Added %s" % nid
        
    def remove_route(self, src, dst):
        """
        removes the route between the given cities from the map
        """
        try:
            self.graph.remove_edge(src, dst)
            return "Removed %s-%s" % (src, dst)
        except:
            return "Error: could not remove %s-%s" % (src, dst)
        
    def add_route(self, src, dst, distance):
        """
        adds a route between the given cities to the map
        """
        try:
            self.graph.add_edge(src, dst, int(distance))
            return "Added %s-%s" % (src, dst)
        except:
            return "Error: could not add %s-%s" % (src, dst)
        
    def edit_city(self, city, field, value):
        """
        updates the given field of the given city with the given value
        """
        try:
            value = eval(value)
        except:
            value = value
            
        try:
            self.graph.node(city).data[field] = value
            return "Updated %s" % city
        except:
            return "Error: could not update %s with given value" % city
        
    def load_extra(self, filename):
        """
        loads extra route and city data into the map
        :param filename: the name of a json data file
        """
        try:
            graph_parser.load_extra(self.graph, filename, symmetric_routes=True)
            return "Loaded %s" % filename
        except:
            return "Error: Could not load %s" % filename
        
    def save(self, filename):
        """
        saves the map data to the given filename in json form
        """
        
        json_dict = dict()
        json_dict["data sources"] = self.data_sources
        
        metros = []
        for city in self.graph.nodes:
            metros.append(city.data)
        json_dict["metros"] = metros
            
        routes = []
        for src in self.graph.node_ids():
            for dst in self.graph.child_ids(src):
                routes.append({
                    "ports": [src, dst],
                    "distance": self.graph.distance_between(src, dst)
                })
        json_dict["routes"] = routes
               
        try: 
            with open(filename, 'w') as save_file:
                json.dump(json_dict, save_file, indent=4)
                save_file.close()
            return "Saved to %s" % filename
        except:
            return "Error: Could not save to %s" % filename
        
    def route_info(self, route):
        """
        :return: info on the provided route, including distance, cost, and time
        :param route: a list of city ids representing a route
        """
        if not self.graph.is_valid_path(route):
            return "Error: Given route is invalid"
        
        distance = self.graph.path_length(route)
        
        current_cost = self.PRICE_PER_KM
        total_cost = 0.0
        for i in range(len(route) - 1):
            if current_cost > 0:
                total_cost += current_cost * self.graph.distance_between(route[i], route[i+1])
                current_cost -= self.CONNECTING_DISCOUNT
            else:
                break
            
        total_time = 0
        for i in range(len(route) - 1):
            d = self.graph.distance_between(route[i], route[i+1])
            if d > 400:
                total_time += (2*self.ACCELERATION_TIME) + ((d - (2*self.ACCELERATION_DISTANCE))/self.PLANE_SPEED)
            else:
                total_time += 2 * sqrt(d / self.PLANE_ACCELERATION)
                
            if i > 0:
                total_time += self._layover_time(route[i])
            
        return  "======== Route info ========\n" + \
                ("Total distance: %s km\n" % distance) + \
                ("Total cost: $%s\n" % round(total_cost, 2)) + \
                ("Total time: %s hours\n" % round(total_time, 2))
                
    def _layover_time(self, city):
        """
        :return: the layover time for the given city
            calculated as 2 hours - 10 minutes * (the number of outbound flights - 1)
        """
        num_outbound = self.graph.out_deg(city)
        return max(0, 2.0 - ((num_outbound - 1) / 6.0))
    
    def shortest_path(self, src, dst):
        """
        :return: the shortest route between src and dst, as well
            as info on that route
        """
        
        path = self.graph.dijkstras(src, dst)
        
        if path == None:
            return "Error: Could not find path between the given cities"
        
        return ("Shortest route: %s\n\n" % '-'.join(path)) + \
                self.route_info(path)     