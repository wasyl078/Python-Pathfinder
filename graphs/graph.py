# imports
from graphs.node import Node
import random
from graphs.edge import Edge
from general.priority_queue import PriorityQueue
import sys
import math
from general.consts_values import Color, Blocks


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

        self.nodes = []
        for i in range(0, columns):
            self.nodes.append([])
            for j in range(0, rows):
                self.nodes[i].append(Node(i, j))

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

    def neighbours_of_v2(self, node):
        neighbours = list()
        # up
        if node.x > 0 and self.matrix.two_dim_list[node.x - 1][node.y].block_type == Blocks.BACKGROUND:
            neighbours.append(self.nodes[node.x - 1][node.y])
        # down
        if node.x < int(self.columns) - 1 and self.matrix.two_dim_list[node.x + 1][node.y].block_type == Blocks.BACKGROUND:
            neighbours.append(self.nodes[node.x + 1][node.y])
        # left
        if node.y > 0 and self.matrix.two_dim_list[node.x][node.y - 1].block_type == Blocks.BACKGROUND:
            neighbours.append(self.nodes[node.x][node.y - 1])
        # right
        if node.y < int(self.rows) - 1 and self.matrix.two_dim_list[node.x][node.y + 1].block_type == Blocks.BACKGROUND:
            neighbours.append(self.nodes[node.x][node.y + 1])

        return neighbours

    # making maze with Prim's algorithm
    def generate_prims_maze(self):
        Q = PriorityQueue(predicate)
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
                    rand_weight = random.randrange(1000)
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

    def reset_parent_nodes(self):
        for i in range(0, self.columns):
            for j in range(0, self.rows):
                self.nodes[i][j].parent_node = None

    def get_lowest_f_cost_from_scores_and_set(self, sett):
        buf = None
        min_cost = sys.maxsize * 2 + 1
        for node in sett:
            if node.f_score < min_cost:
                min_cost = node.f_score
                buf = node

        return buf

    def reconstruct_path(self, node):
        path = list()
        while node is not None:
            path.append(node)
            node = node.parent_node

        for node in path:
            #print(node)
            self.matrix.two_dim_list[node.x][node.y].color = Color.PINK

        self.reset_parent_nodes()
        return path

    def distance(self, node, goal):
        x = node.x - goal.x
        y = node.y - goal.y
        zz = x * x + y * y
        return math.sqrt(zz)

    # A* pathfinding algorithm
    def find_a_star_path(self, start_x, start_y, end_x, end_y):
        start = self.nodes[start_x][start_y]
        goal = self.nodes[end_x][end_y]

        print("szukanie sciezki z: {} -> {}".format(start, goal))

        open_set = set()
        closed_set = set()

        start.g_score = 0

        for neighbour in self.neighbours_of_v2(start):
            open_set.add(neighbour)

        while len(open_set) != 0:
            x = self.get_lowest_f_cost_from_scores_and_set(open_set)

            if goal == x:
                return self.reconstruct_path(goal)

            open_set.remove(x)
            closed_set.add(x)

            for y in self.neighbours_of_v2(x):
                if y in closed_set:
                    continue

                tentative_g_score = x.g_score + self.distance(x, y)
                tentative_is_better = False

                if y not in open_set:
                    open_set.add(y)
                    y.h_score = self.distance(y, goal)
                    tentative_is_better = True
                elif tentative_g_score < y.g_score:
                    tentative_is_better = True

                if tentative_is_better:
                    y.parent_node = x
                    y.g_score = tentative_g_score
                    y.f_score = y.g_score + y.h_score

        print("nie znaleziono drogi")
