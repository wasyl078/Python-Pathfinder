# imports
from graphs.node import Node
import random
from graphs.edge import Edge
from general.priority_queue import PriorityQueue


def predicate(x, y):
    return x.weight < y.weight


# graph is used to generate entry levels by using Prim's algorithm
class MyOwnGraph(object):

    # constructor receives estimated size of graph (width and height)
    # and generates the simplest mesh-like graph
    def __init__(self, matrix, columns, rows):
        self.matrix = matrix
        self.columns = columns
        self.rows = rows

    # finding neighbours of node in graph
    def neighbours_of(self, node):
        neighbours = list()
        # up
        if node.x > 1:
            neighbours.append(Node(node.x - 2, node.y))
        # down
        if node.x < int(self.columns):
            neighbours.append(Node(node.x + 2, node.y))
        # left
        if node.y > 1:
            neighbours.append(Node(node.x, node.y - 2))
        # right
        if node.y < int(self.rows):
            neighbours.append(Node(node.x, node.y + 2))

        return neighbours

    # making maze with Prim's algorithm
    def generate_prims_maze(self):
        Q = PriorityQueue(self.columns * self.rows, predicate)
        visited = {}
        T = list()
        for x in range(0, int(self.columns / 2) + 1):
            for y in range(0, int(self.rows / 2) + 1):
                visited[Node(2 * x, 2 * y)] = False

        visited[Node(0, 0)] = True

        print(visited)

        for node in visited:
            if node == Node(0, 0):
                continue
            for neighbour in self.neighbours_of(node):
                if not visited[neighbour]:
                    rand_weight = random.randrange(3)
                    Q.enqueue(Edge(node, neighbour, rand_weight))

            while not Q.is_empty() and visited[Q.first().node_b]:
                Q.dequeue()

            if not Q.is_empty():
                edge = Q.first()
                node_sr = Node(int((edge.node_b.x + edge.node_a.x) / 2), int((edge.node_a.y + edge.node_b.y) / 2))
                T.append(Edge(edge.node_a, node_sr, 0))
                T.append(Edge(node_sr, edge.node_b, 0))
                visited[edge.node_b] = True

        for edge in T:
            print(edge)
        return T
