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
        self.def_timer = 30
        self.timer = self.def_timer
        self.extra_height = 0
        self.extra_width = 0

    # deals damage to near blocks / objects
    def deal_damage_in_cross(self, mod_x: int, mod_y: int, matrix: Matrix, moveable_objects: List[AbtractBlock]):
        print("boom")
        x = self.pos_x
        y = self.pos_y
        if mod_x > 0 or mod_y > 0:
            new_explosion_right = Explosion(x + mod_x, y)
            new_explosion_left = Explosion(x - mod_x, y)
            new_explosion_down = Explosion(x, y + mod_y)
            new_explosion_up = Explosion(x, y - mod_y)
            moveable_objects.append(new_explosion_right)
            moveable_objects.append(new_explosion_left)
            moveable_objects.append(new_explosion_down)
            moveable_objects.append(new_explosion_up)
            return self.deal_damage_in_cross(max(mod_x - 1, 0), max(mod_y - 1, 0), matrix, moveable_objects)

    # bombs tick - after 100 ticks (1 2/3 sec.) bomb explodes
    @abstractmethod
    def update(self, matrix: Matrix, moveable_objects: List[AbtractBlock]):
        if self.timer <= 0:
            moveable_objects.append(Explosion(self.pos_x, self.pos_y))
            self.deal_damage_in_cross(self.explo_range, self.explo_range, matrix, moveable_objects)
            if self in moveable_objects:
                moveable_objects.remove(self)
        self.timer -= 1

        # color change
        self.color = (self.color[0], self.color[1] - int(255/self.def_timer), self.color[2])

        # size change


    # this method is standard render method - draws square in right place in window
    @abstractmethod
    def render(self, screen: pygame.Surface) -> None:
        buf_rect = pygame.Rect(self.pos_x * self.def_width + self.extra_width,
                               self.pos_y * self.def_height + self.extra_height,
                               self.def_width, self.def_height)
        pygame.draw.rect(screen, self.color, buf_rect)


    # cannot move into bomb block
    @abstractmethod
    def __bool__(self) -> bool:
        return False
