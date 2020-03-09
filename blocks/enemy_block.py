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
        self.last_visited_places = LimitedUniqueStack(20)
        self.bombs_power = 3
        self.def_time_between_moves = 10
        self.timer_to_move = self.def_time_between_moves
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
                self.last_visited_places.push(matrix.two_dim_list[self.pos_x][self.pos_y])
            elif decision == 1:
                self.dec_place_bomb(some_block, matrix, moveable_objects)
                self.last_visited_places.push(matrix.two_dim_list[self.pos_x][self.pos_y])
            elif decision == -1:
                self.dec_escape(some_block, matrix, moveable_objects)
                self.escape_timer = 120
            self.timer_to_move = self.def_time_between_moves

    # finds player to follow (the one, whick is closest to enemy)
    def find_closest_player(self, moveable_objects: List[AbtractBlock]) -> AbtractBlock:
        closest_player = None
        smallest_distance = sys.maxsize * 2 + 1
        for objectt in moveable_objects:
            if objectt.block_type == Blocks.PLAYER:
                buf_dist = self.distance_horizontal(self, objectt)
                if buf_dist < smallest_distance:
                    closest_player = objectt
                    smallest_distance = buf_dist
        if closest_player is None:
            return self
        return closest_player

    # chooses decision: no threat, no enemy in sight - follow path (0, player)
    # bomb in sight - escape (-1, bomb) | player in sight: place bomb (1, player)
    def choose_decison(self, moveable_objects: List[AbtractBlock]) -> Tuple[int, AbtractBlock]:
        # finding threats - biggest priority
        bombs = (elem for elem in moveable_objects if elem.block_type == Blocks.BOMB)
        for bomb in bombs:
            # noinspection PyUnresolvedReferences
            if self.distance_between(self, bomb) < bomb.explo_range:
                return -1, bomb

        # no threats -> check if player is close
        player = self.find_closest_player(moveable_objects)
        if self.distance_horizontal(player, self) < self.bombs_power and self.distance_vertical(player,
                                                                                                self) < self.bombs_power:
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
            self.pos_x = path[-1].x
            self.pos_y = path[-1].y

    # decision: excape - when enemy is in range of bomb
    def dec_escape(self, bomb: Bomb, matrix: Matrix, moveable_objects: List[AbtractBlock]) -> None:
        print("escape")
        last_block = self.last_visited_places.pop()
        if last_block is not None:
            for explo in moveable_objects:
                if explo.block_type == Explosion and last_block.pos_x == explo.pos_x and last_block.pos_y == explo.pos_y:
                    return
            self.pos_x = last_block.pos_x
            self.pos_y = last_block.pos_y
        else:
            save_x, save_y = self.find_close_save_position(matrix)

            for explo in moveable_objects:
                if explo.block_type == Explosion and save_x == explo.pos_x and save_y == explo.pos_y:
                    return

            self.pos_x = save_x
            self.pos_y = save_y

    # decision: place bomb - when player is in range of enemy's attack
    def dec_place_bomb(self, player: Player, matrix: Matrix, moveable_objects: List[AbtractBlock]) -> None:
        print("place")
        moveable_objects.append(Bomb(self.pos_x, self.pos_y, self.bombs_power))

    # calculate distance between two blocks / objects
    def distance_between(self, block_1: AbtractBlock, block_2: AbtractBlock) -> float:
        return sqrt((block_1.pos_x - block_2.pos_x) ** 2 + (block_1.pos_y - block_2.pos_y) ** 2)

    # calculate distance only horizontal
    def distance_horizontal(self, block_1: AbtractBlock, block_2: AbtractBlock):
        return abs(block_1.pos_x - block_2.pos_x)

    # calculate distance only vertical
    def distance_vertical(self, block_1: AbtractBlock, block_2: AbtractBlock):
        return abs(block_1.pos_y - block_2.pos_y)

    # finds close save position: near block that won't explode
    def find_close_save_position(self, matrix: Matrix):
        x = self.pos_x
        y = self.pos_y
        up_block = None
        down_block = None
        left_block = None
        right_block = None
        if matrix.check(x, y - 1):
            up_block = matrix.two_dim_list[x][y - 1]
        if matrix.check(x, y + 1):
            down_block = matrix.two_dim_list[x][y + 1]
        if matrix.check(x - 1, y):
            left_block = matrix.two_dim_list[x - 1][y]
        if matrix.check(x + 1, y):
            right_block = matrix.two_dim_list[x + 1][y]
        # up
        if up_block is not None and (up_block.block_type == Blocks.BACKGROUND):
            return x, y - 1
        # down
        elif down_block is not None and (down_block.block_type == Blocks.BACKGROUND):
            return x, y + 1
        # left
        elif left_block is not None and (left_block.block_type == Blocks.BACKGROUND):
            return x - 1, y
        # right
        elif right_block is not None and (right_block.block_type == Blocks.BACKGROUND):
            return x + 1, y
        else:
            return x, y

    # cannot move into enemy:
    def __bool__(self):
        return False
