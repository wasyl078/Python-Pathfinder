# imports
import pygame
from abc import abstractmethod
from general.consts_values import *
from typing import Tuple


# abstract class for objects contains every important variable for standard block in game
# also contains two abstract methods - update() and render()
class AbtractBlock(object):

    # constructor - defines every variable that will be used in render() and update()
    def __init__(self, posx: int, posy: int, color: Tuple[int, int, int] = Color.RED,
                 block_type: str = Blocks.ABSTRACT, damageable: bool = False) -> None:
        self.pos_x: int = posx
        self.pos_y: int = posy
        self.color: Tuple[int, int, int] = color
        self.block_type: str = block_type
        self.rows: int = NUMBER_OF_OF_BLOCKS[1]
        self.columns: int = NUMBER_OF_OF_BLOCKS[0]
        self.screen_width: int = pygame.display.Info().current_w
        self.screen_height: int = pygame.display.Info().current_h
        self.def_width: float = self.screen_width / self.columns
        self.def_height: float = self.screen_height / self.rows
        self.damageable = damageable

    # this method is supposed to update object's position every clock's tick
    # if necessery - it should be overriden
    @abstractmethod
    def update(self, matrix, moveable_objects) -> None:
        pass

    # this method is standard render method - draws square in right place in window
    @abstractmethod
    def render(self, screen: pygame.Surface) -> None:
        buf_rect = pygame.Rect(self.pos_x * self.def_width,
                               self.pos_y * self.def_height,
                               self.def_width, self.def_height)
        pygame.draw.rect(screen, self.color, buf_rect)

    # this method supports checking if it is possible to move into particular block
    # noinspection PyMethodMayBeStatic
    def check_place(self, posx: int, posy: int, matrix, moveable_objects) -> bool:
        # checking borders
        if posx < 0 or posx > self.columns - 1 or posy < 0 or posy > self.rows - 1:
            return False

        # checking other blocks
        if matrix.two_dim_list[posx][posy]:
            for block in moveable_objects:
                if block.pos_x == posx and block.pos_y == posy and self != block and not block:
                    return False
            return True
        return False

    # overriding __bool_(self) -> True - you can move there, False -> you can't move there
    @abstractmethod
    def __bool__(self) -> bool:
        return True
