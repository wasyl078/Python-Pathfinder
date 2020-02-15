# imports
from abc import abstractmethod
from blocks.abstract_block import AbtractBlock
from framework.consts_values import Color, Blocks


# wall - block in which you can't move into
class Wall(AbtractBlock):
    def __init__(self, posx, posy):
        super().__init__(posx, posy, Color.WHITE, Blocks.WALL)

    # cannot move into wall
    @abstractmethod
    def __bool__(self):
        return False