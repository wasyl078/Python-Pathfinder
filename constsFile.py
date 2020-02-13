# this file only holds const variables, objects used in this project
NUMBER_OF_OF_BLOCKS = (32, 18)


# object holding colours
class Color(object):
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    PINK = (255, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)


# object holding blocks types
class Blocks(object):
    BACKGROUND = "background"
    PLAYER = "player"
    WALL = "wall"
