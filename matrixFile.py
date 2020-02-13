# imports
from backgroundFile import Background
from wallFile import Wall

# matrix class - 2-dimensional table -
# used to check whether position in window is free


class Matrix(object):
    def __init__(self, number_of_rows, number_of_columns):
        self.columns = number_of_columns
        self.rows = number_of_rows
        self.matrix = self.initialize_matrix()

    def initialize_matrix(self):
        matrix = []
        for i in range(0, self.columns):
            matrix.append([])
            for j in range(0, self.rows):
                matrix[i].append(True)
        return matrix

    def set_block_to_background(self, pos_x, pos_y):
        self.matrix[pos_x][pos_y] = Background(pos_x, pos_y)

    def set_block_to_wall(self, pos_x, pos_y):
        self.matrix[pos_x][pos_y] = Wall(pos_x, pos_y)

    def check(self, pos_x, pos_y):
        if pos_x < 0 or pos_x >= self.columns or pos_y < 0 or pos_y >= self.rows:
            return False
        else:
            return bool(self.matrix[pos_x][pos_y])

    def print_only_false(self):
        for i in range(0, self.columns):
            for j in range(0, self.rows):
                if not self.check(i, j):
                    print("{}x{}: {}".format(i, j, self.matrix[i][j].block_type))
