# imports
import sys
from math import sqrt
from blocks.abstract_block import AbtractBlock, abstractmethod
from general.consts_values import Blocks, Color
from general.matrix_of_blocks import Matrix
from blocks.player_block import Player
from typing import List, Tuple
from graphs.graph import MyOwnGraph
from blocks.bomb_block import Bomb
from general.limited_stack import LimitedUniqueStack
from blocks.explosion_block import Explosion


# enemy block / object is always looking for player by using a* pathfinding algorithm
# noinspection PyMethodMayBeStatic
class Enemy(AbtractBlock):

    # constructor - setting enemy object; receives graph
    def __init__(self, pos_x: int, pos_y: int, graph: MyOwnGraph) -> None:
        super().__init__(pos_x, pos_y, Color.PAWEL_PNG, Blocks.ENEMY, True)
        self.graph = graph
        self.bombs_power = 3
        self.def_time_between_moves = 10
        self.timer_to_move = self.def_time_between_moves
        self.def_escape_timer = 120
        self.escape_timer = 0

    # updates position - it depends on player's position
    @abstractmethod
    def update(self, matrix: Matrix, moveable_objects: List[AbtractBlock]) -> None:
        self.update_better_ai(matrix, moveable_objects)

    # update - better AI
    # noinspection PyTypeChecker
    def update_better_ai(self, matrix: Matrix, moveable_objects: List[AbtractBlock]) -> None:
        self.timer_to_move -= 1
        self.escape_timer -= 1
        if self.timer_to_move <= 0:
            decision, some_block = self.choose_decison(moveable_objects)
            if self.escape_timer > 0:
                self.dec_escape(some_block, matrix, moveable_objects)
            elif decision == 0:
                self.dec_move_to_player(some_block, matrix, moveable_objects)
            elif decision == 1:
                self.dec_place_bomb(matrix, moveable_objects)
                self.escape_timer = self.def_escape_timer
            elif decision == -1:
                self.dec_escape(some_block, matrix, moveable_objects)
                if self.escape_timer > 0:
                    self.escape_timer += 30
                else:
                    self.escape_timer = 30
            elif decision == -2:
                self.dec_suicide(matrix, moveable_objects)
            self.timer_to_move = self.def_time_between_moves

    def find_closest_moveable_object(self, block_type: str, moveable_objects: List[AbtractBlock]) -> AbtractBlock:
        closest_moveable_object = None
        smallest_distance = sys.maxsize * 2 + 1
        for objectt in moveable_objects:
            if objectt.block_type == block_type:
                buf_dist = self.distance_between(self, objectt)
                if buf_dist < smallest_distance:
                    closest_moveable_object = objectt
                    smallest_distance = buf_dist
        if closest_moveable_object is not None:
            return closest_moveable_object

    # chooses decision: no threat, no enemy in sight - follow path (0, player)
    # bomb in sight - escape (-1, bomb) | player in sight: place bomb (1, player)
    # no player - suicide (-2, self)
    def choose_decison(self, moveable_objects: List[AbtractBlock]) -> Tuple[int, AbtractBlock]:
        # finding threats - biggest priority
        bombs = (elem for elem in moveable_objects if elem.block_type == Blocks.BOMB)
        for bomb in bombs:
            # noinspection PyUnresolvedReferences
            if self.distance_between(self, bomb) <= bomb.explo_range:
                return -1, bomb

        # no threats -> check if player is close, check if player is not None
        player = self.find_closest_moveable_object(Blocks.PLAYER, moveable_objects)
        if player is None:
            return -2, self
        if self.distance_horizontal(player, self) < self.bombs_power and \
                self.distance_vertical(player, self) < self.bombs_power:
            if (self.pos_x == player.pos_x and self.pos_y != player.pos_y) or \
                    (self.pos_x != player.pos_x and self.pos_y == player.pos_y):
                return 1, player

        # no threats, no players in sight -> move toward player
        return 0, player

    # decision: move towards player - there is no threat
    def dec_move_to_player(self, player: AbtractBlock, matrix: Matrix, moveable_objects: List[AbtractBlock]) -> None:
        print("move")
        path = self.graph.find_a_star_path(self.pos_x, self.pos_y, player.pos_x, player.pos_y)
        if self.check_place(path[-1].x, path[-1].y, matrix, moveable_objects):
            self.try_to_move(path[-1].x, path[-1].y, matrix, moveable_objects)

    # decision: excape - when enemy is in range of bomb
    def dec_escape(self, bomb: Bomb, matrix: Matrix, moveable_objects: List[AbtractBlock]) -> None:
        print("escape {}".format(self.escape_timer))
        x = self.pos_x
        y = self.pos_y
        saver_blocks = [self]
        if self.check(x, y - 1, matrix, moveable_objects):
            saver_blocks.append(matrix.two_dim_list[x][y - 1])
        if self.check(x, y + 1, matrix, moveable_objects):
            saver_blocks.append(matrix.two_dim_list[x][y + 1])
        if self.check(x - 1, y, matrix, moveable_objects):
            saver_blocks.append(matrix.two_dim_list[x - 1][y])
        if self.check(x + 1, y, matrix, moveable_objects):
            saver_blocks.append(matrix.two_dim_list[x + 1][y])
        for block in saver_blocks:
            print("{} -> {}".format(block, self.calculate_position_danger_level(block, matrix, moveable_objects)))
        savest_index = -1
        savest_level = 0
        for i in range(len(saver_blocks)):
            lvl = self.calculate_position_danger_level(saver_blocks[i], matrix, moveable_objects)
            if lvl > savest_level:
                savest_index = i
                savest_level = lvl
        savest_block = saver_blocks[savest_index]
        self.try_to_move_light(savest_block.pos_x, savest_block.pos_y, matrix, moveable_objects)

    def dec_suicide(self, matrix: Matrix, moveable_objects: List[AbtractBlock]):
        for block in moveable_objects:
            if block.block_type == Bomb and block.pos_x == self.pos_x and block.pos_y == self.pos_y:
                return
        self.dec_place_bomb(matrix, moveable_objects)

    # noinspection PyUnresolvedReferences
    def calculate_position_danger_level(self, next_pos: AbtractBlock, matrix: Matrix, moveable_objects: List[AbtractBlock]):
        danger = 0
        for block in moveable_objects:
            if block.block_type == Blocks.PLAYER or block.block_type == Blocks.BOMB or block.block_type == Blocks.EXPLOSION:
                danger += self.distance_between(next_pos, block)
        return danger

    # decision: place bomb - when player is in range of enemy's attack
    def dec_place_bomb(self, matrix: Matrix, moveable_objects: List[AbtractBlock]) -> None:
        print("place")
        moveable_objects.append(Bomb(self.pos_x, self.pos_y, self.bombs_power))

    def get_blocks_objects_on_position(self, x, y, matrix: Matrix, moveable_objects: List[AbtractBlock]):
        blocks = list()
        if not (x < 0 or x >= self.columns or y < 0 or y >= self.rows):
            blocks.append(matrix.two_dim_list[x][y])
        for block in moveable_objects:
            if block.pos_x == x and block.pos_y == y:
                blocks.append(block)
        return blocks

    def try_to_move(self, new_x: int, new_y: int, matrix: Matrix, moveable_objects: List[AbtractBlock]):
        if matrix.checks_blocks_type(new_x, new_y) != Blocks.BACKGROUND:
            return
        for objectt in moveable_objects:
            if objectt.pos_x == new_x and objectt.pos_y == new_y and objectt.block_type == Explosion:
                return
            elif objectt.block_type == Blocks.BOMB:
                # noinspection PyUnresolvedReferences
                if (objectt.pos_x == new_x and self.distance_between(objectt, AbtractBlock(new_x, new_y)) < objectt.explo_range) \
                        or (objectt.pos_y == new_y and self.distance_between(objectt, AbtractBlock(new_x, new_y)) < objectt.explo_range):
                    return

        self.pos_x = new_x
        self.pos_y = new_y

    def try_to_move_light(self, new_x: int, new_y: int, matrix: Matrix, moveable_objects: List[AbtractBlock]):
        for block in moveable_objects:
            if block.block_type == Explosion and block.pos_x == new_x and block.pos_y == new_y:
                return
        self.pos_x = new_x
        self.pos_y = new_y

    def check(self, x, y, matrix: Matrix, moveable_objects: List[AbtractBlock]):
        if x < 0 or x >= self.columns or y < 0 or y >= self.rows:
            return False
        if matrix.two_dim_list[x][y].block_type == Blocks.WALL:
            return False
        for block in moveable_objects:
            if block.pos_x == x and block.pos_y == y:
                if block.block_type == Blocks.PLAYER or block.block_type == Blocks.BOMB:
                    return False
        return True

    # calculate distance between two blocks / objects
    def distance_between(self, block_1: AbtractBlock, block_2: AbtractBlock) -> float:
        return sqrt((block_1.pos_x - block_2.pos_x) ** 2 + (block_1.pos_y - block_2.pos_y) ** 2)

    # calculate distance only horizontal
    def distance_horizontal(self, block_1: AbtractBlock, block_2: AbtractBlock):
        return abs(block_1.pos_x - block_2.pos_x)

    # calculate distance only vertical
    def distance_vertical(self, block_1: AbtractBlock, block_2: AbtractBlock):
        return abs(block_1.pos_y - block_2.pos_y)

    # cannot move into enemy:
    def __bool__(self):
        return False
