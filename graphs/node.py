# imports
from general.consts_values import NUMBER_OF_OF_BLOCKS


# node is just a node in a graph - it contains unique: pos x and pos y


class Node(object):

    # simple constructor with two values
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # overriding of just one equals method
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "Node({}, {})".format(self.x, self.y)

    def __hash__(self):
        return self.x + self.y * NUMBER_OF_OF_BLOCKS[1]
