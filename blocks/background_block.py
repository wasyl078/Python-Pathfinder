# imports
from abc import abstractmethod
from blocks.abstract_block import AbtractBlock
from general.consts_values import Color, Blocks


# background - block in which you can move into without any problem
class Background(AbtractBlock):
    def __init__(self, posx, posy):
        super().__init__(posx, posy, Color.BLACK, Blocks.BACKGROUND)

    # can move in background
    @abstractmethod
    def __bool__(self):
        return True
