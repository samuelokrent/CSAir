# Node: A single node in a graph
class Node:
        
    def __init__(self, nid, data):
        self.nid = nid
        self.data = data
        
    def __hash__(self):
        return hash(self.nid)
    
    def __eq__(self, other):
        return self.nid == other.nid
    
    def __ne__(self, other):
        return self.nid != other.nid
   
# Graph: A class representing the graph ADT     
class Graph:
    
    # node_data: a dictionary whose keys are unique identifiers, and
    # whose values are any data desired to be stored in each node
    def __init__(self, node_data):
        
        # A list of Nodes
        self.nodes = [Node(nid, node_data[nid]) for nid in node_data]
        
        # A mapping from node nid's to their natural number indices
        self._node_indices = dict()
        for index in range(len(self.nodes)):
            self._node_indices[self.nodes[index].nid] = index
            
        # An adjacency matrix
        # edges[i][j] is the length of the edge between nodes i and j
        # or None if they are not adjacent
        self.edges = dict()
        for node in self.nodes:
            self.edges[node.nid] = dict()
            for other_node in self.nodes:
                self.edges[node.nid][other_node.nid] = None
            
    # :return: whether or not the graph contains a node of the given id
    def __contains__(self, node_id):
        return node_id in self.edges
        
    # returns the node with the given id
    def node(self, nid):
        return self.nodes[self.node_index(nid)]
    
    # returns a list of ids of all nodes in the graph
    def node_ids(self):
        return [node.nid for node in self.nodes]
    
    # returns the index in the node list of the given node id
    def node_index(self, nid):
        return self._node_indices[nid]
    
    # returns the length of the edge between the given nodes,
    # or None if they are not connected
    def edge(self, src_nid, dst_nid):
        return self.edges[src_nid][dst_nid]
    
    # adds a new node with the given id and data to the graph
    def add_node(self, nid, data):
        if nid in self:
            return
        
        self.nodes.append(Node(nid, data))
        self._node_indices[nid] = len(self.nodes) - 1
        self.edges[nid] = dict()
        for other_node in self.nodes:
            self.edges[nid][other_node.nid] = None
          
    # updates the given node's data  
    def set_node_data(self, nid, data):
        self.node(nid).data = data
    
    # removes the given node from the graph
    def remove_node(self, nid):
        if nid not in self:
            return
        
        # remove node
        del self.nodes[self.node_index(nid)]
        
        # recalculate index mapping
        del self._node_indices[nid]
        for index in range(len(self.nodes)):
            self._node_indices[self.nodes[index].nid] = index
            
        # remove all edges to/from this node
        for other_node in self.edges:
            del self.edges[other_node][nid]
        del self.edges[nid]
    
    # creates an edge between the given nodes
    def add_edge(self, src_nid, dst_nid, length):
        self.edges[src_nid][dst_nid] = length
        
    # creates edges in both directions between the given nodes
    def add_symmetric_edge(self, n1, n2, length):
        self.add_edge(n1, n2, length)
        self.add_edge(n2, n1, length)
        
    # removes the edge between the given nodes
    def remove_edge(self, src_nid, dst_nid):
        self.edges[src_nid][dst_nid] = None
        
    # returns whether or not the given nodes are connected by an edge
    def is_edge_between(self, src_nid, dst_nid):
        return self.edges[src_nid][dst_nid] != None
    
    # returns the length of the edge between the nodes,
    # or infinity if they are not connected
    def distance_between(self, src_nid, dst_nid):
        if self.is_edge_between(src_nid, dst_nid):
            return self.edge(src_nid, dst_nid)
        else:
            # 2 non-adjacent nodes are infinitely far apart
            return float("inf")
        
    # :return: the length of the given path
    # :param path: a list of node ids that represents the path in question
    def path_length(self, path):
        path_len = 0
        for i in range(len(path) - 1):
            path_len += self.distance_between(path[i], path[i+1])
        return path_len
    
    def is_valid_path(self, path):
        """
        :return: whether path is a connected path in this graph
        :param path: a list of node ids representing a path
        """
        for node in path:
            if node not in self:
                return False
            
        return self.path_length(path) < float("inf")
        
    # returns a list of ids of the given node's child nodes
    def child_ids(self, node_nid):
        return filter(lambda dst: self.edges[node_nid][dst] != None, self.edges[node_nid])
    
    # returns a list of the given node's child nodes
    def children(self, node_nid):
        return [self.node(nid) for nid in self.child_ids(node_nid)]
        
    # returns the out-degree of the given node
    def out_deg(self, node_nid):
        return len(self.children(node_nid))
    
    def dijkstras(self, src, dst):
        """
        runs Dijkstra's shortest path algorithm
        :param src: the start node's id
        :param dst: the end node's id
        :return: a list of node ids representing a minimum path from src to dst
        """
        if not (src in self and dst in self):
            return None
        
        dists = dict()
        parents = dict()
        for node in self.node_ids():
            # dists holds a tuple representing (distance from src, node id, distance is known)
            dists[node] = [float("inf"), node, False]
            # parents maps from a node to its parent in the minimum path
            parents[node] = None
        
        # mark src with a distance of 0
        dists[src][0] = 0
        
        # start with src node
        distance, node, known = dists[src]
        while node != None:
            # mark this node's distance as known
            dists[node][2] = True
            
            # if the destination node's minimum distance is known, we're done
            if node == dst:
                break
            
            # update this node's children's distances
            for other_node in self.child_ids(node):
                new_dist = distance + self.distance_between(node, other_node)
                if new_dist < dists[other_node][0]:
                    dists[other_node][0] = new_dist
                    parents[other_node] = node
                    
            # select next node
            distance, node, known = self._d_select(dists, parents)
            
        # check if destination node's minimum distance was determined
        if not dists[dst][2]:
            return None
        
        # construct path by following parent chain
        path = []
        cur_node = dst
        while cur_node != None:
            path.append(cur_node)
            cur_node = parents[cur_node]
                
        # nodes were added in reverse
        return path[::-1]
        
    def _d_select(self, dists, parents):
        """
        greedily selects the next node to explore in Dijkstra's algorithm.
        selects the node with the minimum current distance that has been reached, 
        but whose minimum distance is not yet known
        """
        tentative_set = filter(lambda node_dist: self._d_is_reached_and_unknown(node_dist, parents), dists.values())
        if len(tentative_set) > 0:
            return min(tentative_set)
        else:
            return (None, None, None)
    
    def _d_is_reached_and_unknown(self, node_dist, parents):
        """
        :return: true if the given node has been reached, but its minimum distance is not known
        """
        return  (parents[node_dist[1]] != None) and (not node_dist[2])