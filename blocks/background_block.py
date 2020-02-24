# imports
from abc import abstractmethod
from blocks.abstract_block import AbtractBlock
from general.consts_values import Color, Blocks


# background - block in which moveable objects can move into without any problems
class Background(AbtractBlock):
    def __init__(self, posx, posy):
        super().__init__(posx, posy, Color.BLACK, Blocks.BACKGROUND)

    # moveable object can indeed move in background
    @abstractmethod
    def __bool__(self):
        return True
