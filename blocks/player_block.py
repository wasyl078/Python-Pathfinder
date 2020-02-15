# imports
import pygame
from blocks.abstract_block import AbtractBlock, abstractmethod
from general.consts_values import Blocks, Color


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

    # another way to handle keyboard events by Player
    def update_single_jump(self, matrix, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            if matrix.check(self.position_x + 1, self.position_y):
                self.position_x += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            if matrix.check(self.position_x - 1, self.position_y):
                self.position_x -= 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            if matrix.check(self.position_x, self.position_y + 1):
                self.position_y += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            if matrix.check(self.position_x, self.position_y - 1):
                self.position_y -= 1

    @abstractmethod
    def render(self, screen):
        super().render(screen)

    @abstractmethod
    def __bool__(self):
        return False
