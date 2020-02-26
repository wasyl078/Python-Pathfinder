# imports
from blocks.abstract_block import AbtractBlock, abstractmethod
from general.consts_values import Blocks, Color
from general.matrix_of_blocks import Matrix
from typing import List


# bomb is an block / object which destroys maze walls and deals damage to moveable objects
class Bomb(AbtractBlock):

    # constructor - bombs are ORANGE
    def __init__(self, pos_x: int, pos_y: int, power) -> None:
        super().__init__(pos_x, pos_y, Color.ORANGE, Blocks.PLAYER)
        self.power = power

    # explosion - damage to walls
    def explosion_walls(self, matrix: Matrix):
        # up
        # down
        # right
        # left
        pass

    # explosion - damage to moveable objects
    def explosion_moveable_objects(self, moveable_objects: List[AbtractBlock]):
        pass

    # bombs tick - after 100 ticks (1 2/3 sec.) bomb explodes
    @abstractmethod
    def update(self, matrix: Matrix, moveable_objects: List[AbtractBlock]):
        # HP check
        if self.HP <= 0:
            moveable_objects.remove(self)

        # bomb explosion - damage dealing to near blocks and objects
        self.HP -= 1
        self.explosion_walls(matrix)
        self.explosion_moveable_objects(moveable_objects)

    # cannot move into bomb block
    @abstractmethod
    def __bool__(self) -> bool:
        return False
