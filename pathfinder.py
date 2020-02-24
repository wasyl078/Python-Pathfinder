# imports
import pygame
import sys
import random
import ctypes
from general.consts_values import NUMBER_OF_OF_BLOCKS, Color
from general.matrix_of_blocks import Matrix
from graphs.graph import MyOwnGraph
from blocks.player_block import Player


# game class - update and render
class Game(object):

    # constructor - creates objects and stores variables
    # also initializes game frame
    def __init__(self) -> None:
        # vars and consts
        self.tps_max = 30.0
        self.game_finished = False
        self.tps_clock = pygame.time.Clock()
        self.tps_delta = 0.0

        # initialization
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.matrix = Matrix(NUMBER_OF_OF_BLOCKS[0], NUMBER_OF_OF_BLOCKS[1])
        self.player = None
        self.moveable_objects = list()
        self.graphh = MyOwnGraph(self.matrix, NUMBER_OF_OF_BLOCKS[0], NUMBER_OF_OF_BLOCKS[1])
        self.initialize_level()
        self.initialize_player()

    # making background blocks2
    def initialize_level(self) -> None:
        T = self.graphh.generate_prims_maze()

        for i in range(0, NUMBER_OF_OF_BLOCKS[0]):
            for j in range(0, NUMBER_OF_OF_BLOCKS[1]):
                self.matrix.set_block_to_wall(i, j)

        # creating maze
        for edge in T:
            x1 = edge.node_a.x
            y1 = edge.node_a.y
            self.matrix.set_block_to_background(x1, y1)
            x2 = edge.node_b.x
            y2 = edge.node_b.y
            self.matrix.set_block_to_background(x2, y2)

        # creating Backgroung window borders
        for i in range(0, NUMBER_OF_OF_BLOCKS[0]):
            self.matrix.set_block_to_background(i, 0)
            self.matrix.set_block_to_background(i, NUMBER_OF_OF_BLOCKS[1] - 1)
        for i in range(0, NUMBER_OF_OF_BLOCKS[1]):
            self.matrix.set_block_to_background(0, i)
            self.matrix.set_block_to_background(NUMBER_OF_OF_BLOCKS[0] - 1, i)

    # placing player in free spot
    def initialize_player(self) -> None:
        x = random.randrange(0, NUMBER_OF_OF_BLOCKS[0])
        y = random.randrange(0, NUMBER_OF_OF_BLOCKS[1])
        if self.matrix.two_dim_list[x][y]:
            self.player = Player(x, y)
            self.moveable_objects.append(self.player)
        else:
            return self.initialize_player()

    # game loop is checking events (from keyboard, window) by calling objects' update()
    # also calls render() and update()
    def game_loop(self) -> None:
        while not self.game_finished:
            # events handling
            # exiting game
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    sys.exit()
                self.player.update_single_jump(self.matrix, event)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.graphh.find_a_star_path(self.player.pos_x, self.player.pos_y, 0, 0)

            # updates handling
            self.tps_delta += self.tps_clock.tick() / 1000.0
            while self.tps_delta > 1 / self.tps_max:
                self.update()
                self.tps_delta -= 1 / self.tps_max

            # render
            self.render()
        sys.exit()

    # updates positions of every object
    def update(self) -> None:
        for i in range(0, NUMBER_OF_OF_BLOCKS[0]):
            for j in range(0, NUMBER_OF_OF_BLOCKS[1]):
                self.matrix.two_dim_list[i][j].update(self.matrix)
        # for object_to_update in self.moveable_objects:
        #     object_to_update.update(self.matrix)

    # drawing every object
    def render(self) -> None:
        self.screen.fill(Color.BLACK)
        for i in range(0, NUMBER_OF_OF_BLOCKS[0]):
            for j in range(0, NUMBER_OF_OF_BLOCKS[1]):
                self.matrix.two_dim_list[i][j].render(self.screen)
        for object_to_render in self.moveable_objects:
            object_to_render.render(self.screen)
        pygame.display.flip()


# avoiding display scalling by windows "maku UI larger / smaller"
ctypes.windll.user32.SetProcessDPIAware()

# starting game:
if __name__ == "__main__":
    actual_game = Game()
    actual_game.game_loop()
