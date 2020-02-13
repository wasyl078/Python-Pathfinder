# imports
import pygame
from abstractObjectFile import AbtractBlock, abstractmethod
from constsFile import Blocks, Color


# player is standard player character
class Player(AbtractBlock):
    # constructor - setting player object
    def __init__(self, posx, posy):
        super().__init__(posx, posy, Color.GREEN, Blocks.PLAYER)

    # player's update is handling keyboard events
    @abstractmethod
    def update(self, matrix):
        keys = pygame.key.get_pressed()
        # input
        if keys[pygame.K_RIGHT] and matrix.check(self.position_x + 1, self.position_y):
            self.position_x += 1
        if keys[pygame.K_LEFT] and matrix.check(self.position_x - 1, self.position_y):
            self.position_x -= 1
        if keys[pygame.K_DOWN] and matrix.check(self.position_x, self.position_y + 1):
            self.position_y += 1
        if keys[pygame.K_UP] and matrix.check(self.position_x, self.position_y - 1):
            self.position_y -= 1

    @abstractmethod
    def render(self, screen):
        super().render(screen)

    @abstractmethod
    def __bool__(self):
        return False
