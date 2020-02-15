# imports
from graphs.node import Node


# graph is used to generate entry levels by using Prim's algorithm
class MyOwnGraph(object):

    # constructor receives size of level (width and height)
    # and generates the simplest mesh-like graph
    def __init__(self, matrix, width, height):
        self.width = width
        self.height = height
        self.nodes_matrix = self.create_nodes_matrix(matrix)

    # creating matrix of nodes - only where there background is
    def create_nodes_matrix(self, matrix):
        buf_matrix = []
        for i in range(0, self.width):
            buf_matrix.append([])
            for j in range(0, self.height):
                if matrix.matrix[i][j]:
                    buf_matrix[i][j] = Node(i, j)
                else:
                    buf_matrix[i][j] = None
        return buf_matrix

    # creating edges between every neighbour node
    def create_edges_matrix(self):
        pass
