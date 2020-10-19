# This is done by me!

"""
You can structure the graph class in any way you like for practice.
You can build the graph using a dictionary to store nodes as keys and a linkedlist of nodes as values.

EX:
class Graphnode:
    def __init__(self, element, edge_val):
        self.element = element
        self.next = None
        self.edge_val = edge_val

class Graph:
    def __init__(self):
        self.nodes = {}
"""

class GraphNode:
    def __init__(self, element):
        self.element = element
        self.children = []

class Edge:
    def __init__(self, from_node, to_node, edge_val):
        self.from_node = from_node
        self.to_node = to_node
        self.edge_val = edge_val

class Graph:
    def __init__(self):
        self.nodes = []

    # This is a helper function that creates directed edges between given nodes.
    def _directed_edge(self, val_1, val_2, exist, edge_val):
        edge_node = Edge(self.nodes[exist[val_1]], self.nodes[exist[val_2]], edge_val)
        self.nodes[exist[val_1]].children.append(edge_node)
        self.nodes[exist[val_2]].children.append(edge_node)
        return self.nodes

    """
    This function creates undirected by default edges between nodes and adds the nodes to the graph
    @param val_1 takes in a value to create the first node.
    @param val_2 takes in a value to create the second.
    @param is_directed: Since this function creates undirected edges, this param can create directed edges. 
    """
    def add(self, val_1, val_2, edge_val, is_directed=False):
        i = 0
        n = len(self.nodes)
        exist = {}
        while i < n:
            exist[self.nodes[i].element] = i 
            i += 1
        if val_1 not in exist:
            node = GraphNode(val_1)
            self.nodes.append(node)
            exist[val_1] = i 
        if val_2 not in exist:
            node_2 = GraphNode(val_2)
            self.nodes.append(node_2)
            exist[val_2] = i
        if exist[val_1] == exist[val_2]:
            exist[val_2] += 1
        if is_directed:
            return self._directed_edge(val_1, val_2, exist, edge_val)
        self.nodes[exist[val_1]].children.append(Edge(self.nodes[exist[val_1]], self.nodes[exist[val_2]], edge_val))
        self.nodes[exist[val_2]].children.append(Edge(self.nodes[exist[val_2]], self.nodes[exist[val_1]], edge_val))
        return self.nodes
        
    
    """
    This function inserts nodes or vertices into the Minimum-Priority-Queue-Heap heap(which is an array).
    Python provides a heap DS that could be used but I decided to bulid my own iteratively.

    @param heap: It's an array that contains a node and the node's distance as a tuple. 
        Example: [
            -> ("D", 9)
        ] 
    @param element: Contains a tuple of a node and the node's distance.
    @param locations: For each time a node gets inserted in the heap I want to be able to know 
    the index of that node in the heap. The reason why is because so I would not have to traverse the heap(array)
    to look for a specific node to do something with it. 
    So the @param is a dic that contains a node as a key and an index(the location of it in the heap) as a value. 
    """
    def insert(self, heap, element, locations):
        heap.append(element)
        return self.siftUp(heap, len(heap)-1, locations)

    """
    @param heap: It's an array that contains a node and the node's distance as a tuple. 
        Example: [
            -> ("D", 9)
        ] 
    @param child: It's an index of a node in the heap
    @param locations: For each time a node gets inserted in the heap I want to be able to know 
    the index of that node in the heap. The reason why is because so I would not have to traverse the heap(array)
    to look for a specific node to do something with it. 
    So the @param is a dic that contains a node as a key and an index(the location of it in the heap) as a value. 
    """
    
    def siftUp(self, heap, child, locations=None):
        parent = parent = (child - 1) // 2
        while child > 0 and heap[child][1] < heap[parent][1]:
            heap[parent], heap[child] = heap[child], heap[parent]
            # locations[heap[child][0]] = child 
            locations[heap[parent][0]] = parent
            child = parent
            parent = (child - 1) //  2
        locations[heap[child][0]] = child
        return heap
        
    """
    This function extracts the smallest node in the heap. It also calls another function "_iterSiftDown" to mantain
    the rules of the heap as Minimum-Priority-Queue-Heap.

    @param heap: It's an array that contains a node and the node's distance as a tuple.
    @param locations:  For each time a node gets inserted in the heap I want to be able to know 
    the index of that node in the heap. The reason why is because so I would not have to traverse the heap(array)
    to look for a specific node to do something with it. 
    So the @param is a dic that contains a node as a key and an index(the location of it in the heap) as a value.
    """
    def extract(self, heap, locations):
        n = len(heap)-1
        min_val = heap[0]
        heap[0] = heap[n]
        locations[heap[n][0]] = 0
        heap.pop()
        self._iterSiftDown(heap, 0, n-1, locations)
        return min_val
    
    """
    This fucntion sifts down the first element in the heap to mantain the heap as Minimum-Priority-Queue-Heap
    @param parent: It's the element that needs to be sifted down.
    @param entries: Is the number of elements that heap containes.
    """
    def _iterSiftDown(self, heap, parent, entries, locations):
        while True:
            left = (2*parent) + 1
            right = left + 1
            if right > entries:
                if left == entries and heap[left][1] < heap[parent][1]:
                    heap[parent][1], heap[left][1] = heap[left][1], heap[parent][1]
                    locations[heap[parent][0]] = parent
                return heap
            elif heap[left][1] < heap[right][1] and heap[left][1] < heap[parent][1]:
                heap[parent], heap[left] = heap[left], heap[parent]
                locations[heap[parent][0]] = parent
                parent = left
            elif heap[right][1] < heap[left][1] and heap[right][1] < heap[parent][1]:
                heap[parent], heap[right] = heap[right], heap[parent]
                locations[heap[parent][0]] = parent
                parent = right
            else:
                return heap
    
    """
    This function finds the shortest path between given nodes.
    @param start_node: It's the node where we start at
    @param goal_node: It's the node that we end at.
    """            
    def dijkstra(self, start_node, goal_node):
        heap = [(start_node, 0)]
        # @var final_dist: Contains the shortes path for each node that we explored.
        final_dist = {}
        locations = {}
        # @var dist_so_far: Check whether or not we visited a specific node.
        dist_so_far = {start_node: 0}
        path_to_node = {start_node: [start_node]}
        i = 0
        n = len(self.nodes)
        while len(heap):
            curr_node = self.extract(heap, locations)
            final_dist[curr_node[0]] = dist_so_far[curr_node[0]]
            del dist_so_far[curr_node[0]]
            del locations[curr_node[0]]
            # nodes = None
            for node in self.nodes:
                if node.element == curr_node[0]:
                    nodes = node.children
                    break
            for node in nodes:
                if node.to_node.element not in final_dist:
                    new_dist = curr_node[1] + node.edge_val
                    if node.to_node.element not in dist_so_far:
                        self.insert(heap, (node.to_node.element, new_dist), locations)
                        dist_so_far[node.to_node.element] = new_dist
                        path_to_node[node.to_node.element] = path_to_node[curr_node[0]] + [node.to_node.element]
        
                    elif new_dist < dist_so_far[node.to_node.element]:
                        dist_so_far[node.to_node.element] = new_dist
                        self.siftUp(heap, locations[node.to_node.element], locations)
                        path_to_node[node.to_node.element] = path_to_node[curr_node[0]] + [node.to_node.element]
            i += 1

        return path_to_node
                    

# g = Graph()
# g.add('A', 'B', 5)
# g.add('A', 'D', 9)
# g.add('A', 'E', 2)
# g.add('C', 'D', 3)
# g.add('D', 'F', 2)
# g.add('E', 'F', 3)
# g.add('B', 'C', 2)

# result = g.dijkstra("A", "D")
# print(result)
# Output: {'A': ['A'], 'E': ['A', 'E'], 'D': ['A', 'E', 'F', 'D'], 'B': ['A', 'B'], 'C': ['A', 'B', 'C'], 'F': ['A', 'E', 'F']}