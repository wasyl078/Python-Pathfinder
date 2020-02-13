# imports
import pygame
import sys
import random
from playerFile import Player
from matrixFile import Matrix
from constsFile import NUMBER_OF_OF_BLOCKS, Color


# game class - update and render
class Game(object):

    # constructor - creates objects and stores variables
    # also initializes game frame
    def __init__(self):
        # vars and consts
        self.tps_max = 30.0
        self.game_finished = False
        self.tps_clock = pygame.time.Clock()
        self.tps_delta = 0.0

        # initialization
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.matrix = Matrix(NUMBER_OF_OF_BLOCKS[1], NUMBER_OF_OF_BLOCKS[0])
        self.moveable_objects = [Player(0, 0)]
        self.initizalize_level()

    # making background blocks
    def initizalize_level(self):
        for i in range(0, NUMBER_OF_OF_BLOCKS[0]):
            for j in range(0, NUMBER_OF_OF_BLOCKS[1]):
                if random.randrange(10) > 1:
                    self.matrix.set_block_to_background(i, j)
                else:
                    self.matrix.set_block_to_wall(i, j)

    # game loop is checking events (from keyboard, window) by calling objects' update()
    # also calls render() and update()
    def game_loop(self):
        while not self.game_finished:
            # events handling
            # exiting game
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    sys.exit()

            # updates handling
            self.tps_delta += self.tps_clock.tick() / 1000.0
            while self.tps_delta > 1 / self.tps_max:
                self.update()
                self.tps_delta -= 1 / self.tps_max

            # render
            self.render()
        sys.exit()

    # updates positions of every object
    def update(self):
        for i in range(0, NUMBER_OF_OF_BLOCKS[0]):
            for j in range(0, NUMBER_OF_OF_BLOCKS[1]):
                self.matrix.matrix[i][j].update(self.matrix)
        for object_to_update in self.moveable_objects:
            object_to_update.update(self.matrix)

    # drawing every object
    def render(self):
        self.screen.fill(Color.PINK)
        for i in range(0, NUMBER_OF_OF_BLOCKS[0]):
            for j in range(0, NUMBER_OF_OF_BLOCKS[1]):
                self.matrix.matrix[i][j].render(self.screen)
        for object_to_render in self.moveable_objects:
            object_to_render.render(self.screen)
        pygame.display.flip()


# staring game
if __name__ == "__main__":
    actual_game = Game()
    actual_game.game_loop()
