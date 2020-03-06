# imports
import pygame

# this file only holds const values and class used in this project
NUMBER_OF_OF_BLOCKS = (64, 36)


# class holding colours
class Color(object):
    RED = (255, 0, 0)
    DARK_ORANGE = (255, 64, 0)
    ORANGE = (255, 128, 0)
    YELLOW = (255, 255, 0)
    MEGA_LIGHT_GREEN = (191, 255, 0)
    GREEN = (0, 255, 0)
    CYAN = (0, 255, 128)
    LIGHT_BLUE = (0, 255, 255)
    BLUE = (0, 0, 255)
    PURPLE = (128, 0, 255)
    PINK = (255, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    LUKASZ_IMG = pygame.image.load("pictures/lukasz lewo.png")
    PIZZA_IMG = pygame.image.load("pictures/pizza.png")
    UFO_IMG = pygame.image.load("pictures/ufo.png")
    ANDROID_PNG = pygame.image.load("pictures/android.png")
    PAWEL_PNG = pygame.image.load("pictures/pawel.png")
    OGOREK_PNG = pygame.image.load("pictures/ogorek.png")
    playable_colors_list = [DARK_ORANGE, ORANGE, YELLOW, MEGA_LIGHT_GREEN, GREEN, CYAN, LIGHT_BLUE, BLUE, PURPLE, PINK,
                            LUKASZ_IMG, PIZZA_IMG, UFO_IMG, ANDROID_PNG, PAWEL_PNG, OGOREK_PNG]


# object holding blocks2 types
class Blocks(object):
    ABSTRACT = "None"
    BACKGROUND = "background"
    PLAYER = "player"
    WALL = "wall"
    ENEMY = "enemy"
    PATH = "path"
    BOMB = "bomb"
    EXPLOSION = "explosion"
