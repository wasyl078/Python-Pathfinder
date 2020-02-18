# imports
import pygame
from abc import abstractmethod
from general.consts_values import *


# abstract class for objects contains every important variables for standard block in game
# also contains two abstract methods - update() and render()
class AbtractBlock(object):
    def __init__(self, posx, posy, color, block_type):
        self.position_x = posx
        self.position_y = posy
        self.color = color
        self.block_type = block_type
        self.blocks_rows = NUMBER_OF_OF_BLOCKS[1]
        self.blocks_columns = NUMBER_OF_OF_BLOCKS[0]
        width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.screen_width = width
        self.screen_height = height
        self.default_width = self.screen_width / self.blocks_columns
        self.default_height = self.screen_height / self.blocks_rows

    # this method is supposed to update object's position every clock's tick
    @abstractmethod
    def update(self, matrix):
        pass

    # this method is supposed to render object in window
    @abstractmethod
    def render(self, screen):
        buf_rect = pygame.Rect(self.position_x * self.default_width,
                               self.position_y * self.default_height, self.default_width, self.default_height)
        pygame.draw.rect(screen, self.color, buf_rect)

    # overriding __bool_(self) -> True - you can move there, False -> you can't move there
    @abstractmethod
    def __bool__(self):
        return True