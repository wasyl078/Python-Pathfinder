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


class Enemy(AbtractBlock):

    def __init__(self, pos_x: int, pos_y: int, graph: MyOwnGraph) -> None:
        super().__init__(pos_x, pos_y, Color.PAWEL_PNG, Blocks.ENEMY, True)
        self.graph = graph
        self.last_visited_places = LimitedUniqueStack(20)
        self.bombs_power = 3
        self.def_time_between_moves = 10
        self.timer_to_move = self.def_time_between_moves
        self.escape_timer = 0

    @abstractmethod
    def update(self, matrix: Matrix, moveable_objects: List[AbtractBlock]) -> None:
        self.make_decision()

    def try_to_change_position(self, new_x: int, new_y: int, matrix: Matrix, moveable_objects: List[AbtractBlock]):
        if matrix.checks_blocks_type(new_x, new_y) != Blocks.BACKGROUND:
            return
        for objectt in moveable_objects:
            if objectt.pos_x == new_x and objectt.pos_y == new_y and objectt.block_type == Explosion:
                return
            elif objectt.block_type == Blocks.BOMB:
                # noinspection PyUnresolvedReferences
                if objectt.pos_x == new_x and self.distance(objectt, AbtractBlock(new_x, new_y)) < objectt.explo_range:
                    return
                elif objectt.pos_y == new_y and self.distance(objectt, AbtractBlock(new_x, new_y)) < objectt.explo_range:
                    return

        self.pos_x = new_x
        self.pos_y = new_y

    def make_decision(self, matrix: Matrix, moveable_objects: List[AbtractBlock]):
        player = self.find_closest_player(moveable_objects)
        bomb = self.find_closest_bomb(moveable_objects)


    def find_closest_player(self, moveable_objects: List[AbtractBlock]) -> AbtractBlock:
        closest_player = None
        smallest_distance = sys.maxsize * 2 + 1
        for objectt in moveable_objects:
            if objectt.block_type == Blocks.PLAYER:
                buf_dist = self.distance(self, objectt)
                if buf_dist < smallest_distance:
                    closest_player = objectt
                    smallest_distance = buf_dist
        if closest_player is None:
            return self
        return closest_player

    def distance(self, object_a: AbtractBlock, object_b: AbtractBlock):
        return sqrt((object_a.pos_x - object_b.pos_x) ** 2 + (object_a.pos_y - object_b.pos_y) ** 2)

    def __bool__(self):
        return False
