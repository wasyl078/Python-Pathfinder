# this file only holds const values and class used in this project
NUMBER_OF_OF_BLOCKS = (64, 36)


# class holding colours
class Color(object):
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    PINK = (255, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    ORANGE = (255, 165, 0)


# object holding blocks2 types
class Blocks(object):
    ABSTRACT = "None"
    BACKGROUND = "background"
    PLAYER = "player"
    WALL = "wall"
    ENEMY = "enemy"
    PATH = "path"
    BOMB = "bomb"
