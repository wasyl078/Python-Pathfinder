# imports
from abc import abstractmethod
from blocks.abstract_block import AbtractBlock
from general.consts_values import Color, Blocks


# wall - block in which you can't move into
class Wall(AbtractBlock):
    def __init__(self, pos_x: int, pos_y: int) -> None:
        super().__init__(pos_x, pos_y, Color.WHITE, Blocks.WALL)

    # cannot move into wall
    @abstractmethod
    def __bool__(self) -> bool:
        return False
