# imports
from general.consts_values import NUMBER_OF_OF_BLOCKS


# node is just a node in a graph - it contains unique: position x and position y
class Node(object):

    # simple constructor with two values
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y
        # noinspection PyTypeChecker
        self.parent_node: Node = None
        self.g_score: float = 0
        self.f_score: float = 0
        self.h_score: float = 0

    # overriding of equal method - checks x and y
    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    # overriding str method -> better printing
    def __str__(self) -> str:
        return "Node({}, {})".format(self.x, self.y)

    # overriding hash method
    def __hash__(self) -> int:
        return self.x + self.y * NUMBER_OF_OF_BLOCKS[1]
