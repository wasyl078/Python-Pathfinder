# imports
from blocks.background_block import Background
from blocks.wall_block import Wall


# matrix class - 2-dimensional list used to check whether position in window is free
class Matrix(object):
    def __init__(self, number_of_columns, number_of_rows):
        self.columns = number_of_columns
        self.rows = number_of_rows
        self.two_dim_list = [[None for x in range(self.rows)] for y in range(self.columns)]

    def set_block_to_background(self, pos_x, pos_y):
        if pos_x < 0 or pos_x > self.columns - 1 or pos_y < 0 or pos_y > self.rows - 1:
            return
        self.two_dim_list[pos_x][pos_y] = Background(pos_x, pos_y)

    def set_block_to_wall(self, pos_x, pos_y):
        if pos_x < 0 or pos_x > self.columns - 1 or pos_y < 0 or pos_y > self.rows - 1:
            return
        self.two_dim_list[pos_x][pos_y] = Wall(pos_x, pos_y)

    def check(self, pos_x, pos_y):
        if pos_x < 0 or pos_x >= self.columns or pos_y < 0 or pos_y >= self.rows:
            return False
        else:
            return bool(self.two_dim_list[pos_x][pos_y])

    def print_only_false(self):
        for i in range(0, self.columns):
            for j in range(0, self.rows):
                if not self.check(i, j):
                    print("{}x{}: {}".format(i, j, self.two_dim_list[i][j].block_type))
