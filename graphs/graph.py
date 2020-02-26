# imports
from graphs.node import Node
import random
from graphs.edge import Edge
from general.priority_queue import PriorityQueue
import sys
import math
from general.consts_values import Color, Blocks
from typing import List, Set
from general.matrix_of_blocks import Matrix
from blocks.abstract_block import AbtractBlock


# graph is used to generate entry levels by using Prim's algorithm
class MyOwnGraph(object):

    # constructor receives estimated size of graph (width and height)
    # and generates the simplest mesh-like graph
    def __init__(self, matrix: Matrix, columns: int, rows: int) -> None:
        self.two_dim_list: List[List[AbtractBlock]] = matrix.two_dim_list
        self.columns: int = columns
        self.rows: int = rows
        self.nodes: List[List[Node]] = [[Node(y, x) for x in range(rows)] for y in range(columns)]

    # ------------------------------makes maze with Prim's algorithm --------------------------------------------------
    def generate_prims_maze(self) -> List[Edge]:
        edge_queue = PriorityQueue(self.ascending_edge_order)
        visited = {}
        T = list()
        for x in range(0, int(self.columns / 2) + 1):
            for y in range(0, int(self.rows / 2) + 1):
                visited[Node(2 * x, 2 * y)] = False

        for node in visited:
            for neighbour in self.range_2_neighbours_of_(node):
                if not visited[neighbour]:
                    edge_queue.enqueue(Edge(node, neighbour, random.randrange(1000)))

            while not edge_queue.is_empty() and visited[edge_queue.first().node_b]:
                edge_queue.dequeue()

            if not edge_queue.is_empty():
                edge = edge_queue.first()
                node_sr = Node(int((edge.node_b.x + edge.node_a.x) / 2), int((edge.node_a.y + edge.node_b.y) / 2))
                T.append(Edge(edge.node_a, node_sr, 0))
                T.append(Edge(node_sr, edge.node_b, 0))
                visited[edge.node_b] = True
        return T

    # finds neighbours of node in graph in range of 2 blocks only
    def range_2_neighbours_of_(self, node: Node) -> List[Node]:
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

    # this function make sure, that priority queue in generate_prims_maze() will be ascending
    # noinspection PyMethodMayBeStatic
    def ascending_edge_order(self, x: Edge, y: Edge) -> bool:
        return x.weight < y.weight

    # -----------------------------------A* pathfinding algorithm ------------------------------------------------------
    def find_a_star_path(self, start_x: int, start_y: int, end_x: int, end_y: int) -> List[Node]:
        start = self.nodes[start_x][start_y]
        goal = self.nodes[end_x][end_y]

        open_set = set()
        closed_set = set()

        start.g_score = 0

        for neighbour in self.close_neighbours_of(start):
            open_set.add(neighbour)

        while len(open_set) != 0:
            x = self.get_lowest_f_cost_from_scores_and_set(open_set)

            if goal == x:
                return self.reconstruct_path(goal)

            open_set.remove(x)
            closed_set.add(x)

            for y in self.close_neighbours_of(x):
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

    # finds closests neighbours of node in graph (in range of 1 block only)
    def close_neighbours_of(self, node):
        neighbours = list()
        # up
        if node.x > 0 and self.two_dim_list[node.x - 1][node.y].block_type == Blocks.BACKGROUND:
            neighbours.append(self.nodes[node.x - 1][node.y])
        # down
        if node.x < int(self.columns) - 1 and self.two_dim_list[node.x + 1][node.y].block_type == Blocks.BACKGROUND:
            neighbours.append(self.nodes[node.x + 1][node.y])
        # left
        if node.y > 0 and self.two_dim_list[node.x][node.y - 1].block_type == Blocks.BACKGROUND:
            neighbours.append(self.nodes[node.x][node.y - 1])
        # right
        if node.y < int(self.rows) - 1 and self.two_dim_list[node.x][node.y + 1].block_type == Blocks.BACKGROUND:
            neighbours.append(self.nodes[node.x][node.y + 1])
        return neighbours

    # deletes parents in graph nodes, becouse of that we can use same nodes in futere path finding calls
    def reset_parent_nodes(self):
        for i in range(0, self.columns):
            for j in range(0, self.rows):
                self.nodes[i][j].parent_node = None

    # finds node with lowest f cost in the set
    # noinspection PyMethodMayBeStatic
    def get_lowest_f_cost_from_scores_and_set(self, the_set: Set[Node]) -> Node:
        buf = None
        min_cost = sys.maxsize * 2 + 1
        for node in the_set:
            if node.f_score < min_cost:
                min_cost = node.f_score
                buf = node
        return buf

    # creates list of node from each nodes' parents
    def reconstruct_path(self, node: Node) -> List[Node]:
        path = list()
        while node is not None:
            path.append(node)
            node = node.parent_node
        # colouring path
        # for node in path:
        #     self.two_dim_list[node.x][node.y].color = Color.PINK

        self.reset_parent_nodes()
        return path

    # calculates distance between two nodes
    # noinspection PyMethodMayBeStatic
    def distance(self, node: Node, goal: Node) -> float:
        x = node.x - goal.x
        y = node.y - goal.y
        zz = x * x + y * y
        return math.sqrt(zz)
