# imports
from blocks.abstract_block import AbtractBlock, abstractmethod
from general.consts_values import Blocks, Color
from general.matrix_of_blocks import Matrix
from typing import List


# bomb is an block / object which destroys maze walls and deals damage to moveable objects
class Bomb(AbtractBlock):
    def __init__(self, pos_x: int, pos_y: int) -> None:
        super().__init__(pos_x, pos_y, Color.ORANGE, Blocks.PLAYER)

    # cannot
    @abstractmethod
    def update(self, matrix:Matrix, moveable_objects: List[AbtractBlock]):
        pass

    # cannot move into bomb block
    @abstractmethod
    def __bool__(self) -> bool:
        return False
