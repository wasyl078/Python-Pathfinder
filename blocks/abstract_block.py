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
                 block_type: str = Blocks.ABSTRACT) -> None:
        self.pos_x: int = posx
        self.pos_y: int = posy
        self.color: Tuple[int, int, int] = color
        self.block_type: str = block_type
        self.row: int = NUMBER_OF_OF_BLOCKS[1]
        self.column: int = NUMBER_OF_OF_BLOCKS[0]
        self.screen_width: int = pygame.display.Info().current_w
        self.screen_height: int = pygame.display.Info().current_h
        self.def_width: float = self.screen_width / self.column
        self.def_height: float = self.screen_height / self.row

    # this method is supposed to update object's position every clock's tick
    # if necessery - it should be overriden
    @abstractmethod
    def update(self, matrix) -> None:
        pass

    # this method is standard render method - draws square in right place in window
    @abstractmethod
    def render(self, screen: pygame.Surface) -> None:
        buf_rect = pygame.Rect(self.pos_x * self.def_width,
                               self.pos_y * self.def_height,
                               self.def_width, self.def_height)
        pygame.draw.rect(screen, self.color, buf_rect)

    # overriding __bool_(self) -> True - you can move there, False -> you can't move there
    @abstractmethod
    def __bool__(self) -> bool:
        return True
