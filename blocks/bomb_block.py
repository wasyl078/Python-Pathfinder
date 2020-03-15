# imports
from blocks.abstract_block import AbtractBlock, abstractmethod
from general.consts_values import Blocks, Color
from general.matrix_of_blocks import Matrix
from blocks.explosion_block import Explosion
from typing import List
import pygame


# bomb is an block / object which destroys maze walls and deals damage to moveable objects
class Bomb(AbtractBlock):

    # constructor - bombs creates explosions when trigerred or when their timer goes to zero
    def __init__(self, pos_x: int, pos_y: int, explo_range):
        super().__init__(pos_x, pos_y, Color.YELLOW, Blocks.BOMB, True)
        self.explo_range = explo_range
        self.__def_timer = 90
        self.timer = self.__def_timer
        self.__extra_height = 0
        self.__extra_width = 0
        self.__width = 0
        self.__height = 0

    # bombs tick - after 90 ticks (1 1/2 sec.) bomb explodes
    @abstractmethod
    def update(self, matrix: Matrix, moveable_objects: List[AbtractBlock]):
        self.color_size_update()
        if self.timer <= 0:
            self.explode(matrix, moveable_objects)
        self.timer -= 1

    # if timer goes to zero, then bomb explodes
    def explode(self, matrix: Matrix, moveable_objects: List[AbtractBlock]):
        self.deal_damage_in_cross(matrix, moveable_objects)
        if self in moveable_objects:
            moveable_objects.remove(self)

    # bomb changes its size and color while loading
    def color_size_update(self):
        self.color = (self.color[0], self.color[1] - int(255 / self.__def_timer), self.color[2])
        self.__extra_width = int(self.def_width / 2) - int((1 - self.timer / self.__def_timer) * self.def_width / 2)
        self.__extra_height = int(self.def_height / 2) - int((1 - self.timer / self.__def_timer) * self.def_height / 2)
        self.__width = int((1 - self.timer / self.__def_timer) * self.def_width)
        self.__height = int((1 - self.timer / self.__def_timer) * self.def_height)

    # deals damage to near blocks / objects
    def deal_damage_in_cross(self, matrix: Matrix, moveable_objects: List[AbtractBlock]):
        moveable_objects.append(Explosion(self.pos_x, self.pos_y))
        self.deal_damage_to(0, 1, matrix, moveable_objects)
        self.deal_damage_to(0, -1, matrix, moveable_objects)
        self.deal_damage_to(1, 0, matrix, moveable_objects)
        self.deal_damage_to(-1, 0, matrix, moveable_objects)

    # deals damage to particular directttion -> till counters wall block
    def deal_damage_to(self, mod_x: int, mod_y: int, matrix: Matrix, moveable_objects: List[AbtractBlock]):
        for i in range(0, self.explo_range):
            moveable_objects.append(Explosion(self.pos_x + mod_x * (i + 1), self.pos_y + mod_y * (i + 1)))
            if matrix.checks_blocks_type(self.pos_x + mod_x * (i + 1), self.pos_y + mod_y * (i + 1)) == Blocks.WALL:
                break

    # this method is special render method - bombs is small and gets bigger with time
    @abstractmethod
    def render(self, screen: pygame.Surface) -> None:
        buf_rect = pygame.Rect(self.pos_x * self.def_width + self.__extra_width,
                               self.pos_y * self.def_height + self.__extra_height,
                               self.__width, self.__height)
        pygame.draw.rect(screen, self.color, buf_rect)

    # cannot move into bomb block
    @abstractmethod
    def __bool__(self):
        return False
