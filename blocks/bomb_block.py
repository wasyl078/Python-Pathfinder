# imports
from blocks.abstract_block import AbtractBlock, abstractmethod
from general.consts_values import Blocks, Color
from general.matrix_of_blocks import Matrix
from blocks.explosion_block import Explosion
from typing import List
import pygame


# bomb is an block / object which destroys maze walls and deals damage to moveable objects
class Bomb(AbtractBlock):

    # constructor - bombs are from YELLOW TO RED
    def __init__(self, pos_x: int, pos_y: int, explo_range) -> None:
        super().__init__(pos_x, pos_y, Color.YELLOW, Blocks.BOMB, True)
        self.explo_range = explo_range
        self.def_timer = 90
        self.timer = self.def_timer
        self.extra_height = 0
        self.extra_width = 0
        self.width = 0
        self.height = 0

    # deals damage to near blocks / objects
    def deal_damage_in_cross(self, matrix: Matrix, moveable_objects: List[AbtractBlock]):
        moveable_objects.append(Explosion(self.pos_x, self.pos_y))
        self.deal_damage_to("up", matrix, moveable_objects)
        self.deal_damage_to("down", matrix, moveable_objects)
        self.deal_damage_to("left", matrix, moveable_objects)
        self.deal_damage_to("right", matrix, moveable_objects)

    # deals damage to particular direction -> till counters wall block
    def deal_damage_to(self, direction: str, matrix: Matrix, moveable_objects: List[AbtractBlock]):
        x = self.pos_x
        y = self.pos_y
        if direction == "up":
            for i in range(0, self.explo_range):
                moveable_objects.append(Explosion(x, y - i - 1))
                if matrix.checks_blocks_type(x, y - i - 1) == Blocks.WALL:
                    break
        elif direction == "down":
            for i in range(0, self.explo_range):
                moveable_objects.append(Explosion(x, y + i + 1))
                if matrix.checks_blocks_type(x, y + i + 1) == Blocks.WALL:
                    break
        elif direction == "left":
            for i in range(0, self.explo_range):
                moveable_objects.append(Explosion(x - i - 1, y))
                if matrix.checks_blocks_type(x - i - 1, y) == Blocks.WALL:
                    break
        elif direction == "right":
            for i in range(0, self.explo_range):
                moveable_objects.append(Explosion(x + i + 1, y))
                if matrix.checks_blocks_type(x + i + 1, y) == Blocks.WALL:
                    break

    # bombs tick - after 100 ticks (1 2/3 sec.) bomb explodes
    @abstractmethod
    def update(self, matrix: Matrix, moveable_objects: List[AbtractBlock]):
        if self.timer <= 0:
            self.deal_damage_in_cross(matrix, moveable_objects)
            if self in moveable_objects:
                moveable_objects.remove(self)
        self.timer -= 1

        # color change
        self.color = (self.color[0], self.color[1] - int(255 / self.def_timer), self.color[2])

        # size change
        self.extra_width = int(self.def_width / 2) - int((1 - self.timer / self.def_timer) * self.def_width / 2)
        self.extra_height = int(self.def_height / 2) - int((1 - self.timer / self.def_timer) * self.def_height / 2)
        self.width = int((1 - self.timer / self.def_timer) * self.def_width)
        self.height = int((1 - self.timer / self.def_timer) * self.def_height)

    # this method is standard render method - draws square in right place in window
    @abstractmethod
    def render(self, screen: pygame.Surface) -> None:
        buf_rect = pygame.Rect(self.pos_x * self.def_width + self.extra_width,
                               self.pos_y * self.def_height + self.extra_height,
                               self.width, self.height)
        pygame.draw.rect(screen, self.color, buf_rect)

    # cannot move into bomb block
    @abstractmethod
    def __bool__(self) -> bool:
        return False
