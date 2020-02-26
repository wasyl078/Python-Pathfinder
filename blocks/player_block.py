# imports
import pygame
from blocks.abstract_block import AbtractBlock, abstractmethod
from general.consts_values import Blocks, Color
from general.matrix_of_blocks import Matrix
from typing import List


# player is an actual object that user control
class Player(AbtractBlock):

    # constructor - setting player object
    def __init__(self, pos_x: int, pos_y: int) -> None:
        super().__init__(pos_x, pos_y, Color.GREEN, Blocks.PLAYER)

    # player's update is handling keyboard events
    @abstractmethod
    def update(self, matrix: Matrix, moveable_objects: List[AbtractBlock]) -> None:
        return
        keys = pygame.key.get_pressed()
        # input
        if keys[pygame.K_RIGHT] and matrix.check(self.pos_x + 1, self.pos_y):
            self.pos_x += 1
        if keys[pygame.K_LEFT] and matrix.check(self.pos_x - 1, self.pos_y):
            self.pos_x -= 1
        if keys[pygame.K_DOWN] and matrix.check(self.pos_x, self.pos_y + 1):
            self.pos_y += 1
        if keys[pygame.K_UP] and matrix.check(self.pos_x, self.pos_y - 1):
            self.pos_y -= 1

    # another way to handle keyboard events by Player
    def update_single_jump(self, matrix: Matrix, moveable_objects: List[AbtractBlock], event: pygame.event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            if self.check_place(self.pos_x + 1, self.pos_y, matrix, moveable_objects):
                self.pos_x += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            if self.check_place(self.pos_x - 1, self.pos_y, matrix, moveable_objects):
                self.pos_x -= 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            if self.check_place(self.pos_x, self.pos_y + 1, matrix, moveable_objects):
                self.pos_y += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            if self.check_place(self.pos_x, self.pos_y - 1, matrix, moveable_objects):
                self.pos_y -= 1

    # cannot move into player block
    @abstractmethod
    def __bool__(self) -> bool:
        return False
