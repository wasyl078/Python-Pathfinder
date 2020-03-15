# imports
from graphs.node import Node


# edge - in a graph - contains two nodes and edge's weight
class Edge(object):

    # constructor with two nodes and weight
    def __init__(self, node_a: Node, node_b: Node, weight: int):
        self.node_a: Node = node_b
        self.node_b: Node = node_a
        self.weight: int = weight

    # overriding of eqauls method
    def __eq__(self, other):
        return self.node_a == other.node_a and self.node_b == other.node_b and self.weight == other.weight

    # overriding str method -> better edges printing
    def __str__(self):
        return "{}  <-->  {}  |  w: {}".format(self.node_a, self.node_b, self.weight)
