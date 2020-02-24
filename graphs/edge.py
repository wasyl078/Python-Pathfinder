# imports


# edge - in a graph - contains two nodes and weight
class Edge(object):

    # constructor with two nodes and weight
    def __init__(self, node_a, node_b, weight):

        self.node_a = node_b
        self.node_b = node_a
        self.weight = weight

    def get_node_a(self):
        return self.node_a

    def get_node_b(self):
        return self.node_b

    # overriding of eqauls method
    def __eq__(self, other):
        return self.node_a == other.node_a and self.node_b == other.node_b and self.weight == other.weight

    def __str__(self):
        return "{}  <-->  {}  |  w: {}".format(self.node_a, self.node_b, self.weight)
