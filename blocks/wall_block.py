# imports
from abc import abstractmethod
from blocks.abstract_block import AbtractBlock
from general.consts_values import Color, Blocks
from typing import List


# wall - block in which you can't move into
class Wall(AbtractBlock):

    # constructor sets walls to WHITE color
    def __init__(self, pos_x: int, pos_y: int) -> None:
        super().__init__(pos_x, pos_y, Color.WHITE, Blocks.WALL)

    # walls may be destroyed
    @abstractmethod
    def update(self, matrix, moveable_objects: List[AbtractBlock]) -> None:
        if self.HP <= 0:
            matrix.set_block_to_background(self.pos_x, self.pos_y)

    # cannot move into wall
    @abstractmethod
    def __bool__(self) -> bool:
        return False
