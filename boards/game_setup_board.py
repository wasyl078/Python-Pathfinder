import pygame
from general.consts_values import Color
from typing import Tuple
import sys


# this is first thing you see when game starts - player icon choice menu
class GameSetup(object):

    # constructor - creates variables and initialize menu
    def __init__(self):
        self.__tps_max = 30.0
        self.__choosen_color = None
        self.__tps_clock = pygame.time.Clock()
        self.__tps_delta = 0.0
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width: int = pygame.display.Info().current_w
        self.screen_height: int = pygame.display.Info().current_h
        self.color_rectangles = list()
        self.initialize_color_rectangles()

    # "menu game" loop, returns user's choice
    def game_setup_loop(self) -> str:
        while self.__choosen_color is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    sys.exit()  # press ESC to exit menu
            self.__tps_delta += self.__tps_clock.tick() / 1000.0
            while self.__tps_delta > 1 / self.__tps_max:
                self.update()
                self.__tps_delta -= 1 / self.__tps_max
            self.render()
        return self.__choosen_color

    # uses list of choices (from consts_values.py) to visualise these icon for user
    def initialize_color_rectangles(self):
        x = self.screen_width / 5
        y = self.screen_height * 5 / 10
        def_side = self.screen_width / 30
        for color in Color.playable_colors_list:
            buf_rect = PngOrColorRectangle(x, y, def_side, def_side, color)
            self.color_rectangles.append(buf_rect)
            x += self.screen_width / 5
            if x == self.screen_width:
                x = self.screen_width / 5
                y += self.screen_height / 10

    # checks mouse position - player click on icon -> this is the choosen icon for Player Block
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for color_rect in self.color_rectangles:
            if color_rect.check_collide_point(mouse_pos):
                self.__choosen_color = color_rect.color_or_picture

    # renders icons and background image
    def render(self):
        self.screen.fill(Color.BLACK)
        img = pygame.image.load("pictures/pathfinder menu v2.png")
        img = pygame.transform.scale(img, (self.screen_width, self.screen_height))
        self.screen.blit(img, (0, 0))
        for color_rect in self.color_rectangles:
            color_rect.draw_rect(self.screen)
        pygame.display.flip()


# class for icons that you can see in menu
class PngOrColorRectangle(object):
    # constructon - variables and initialization of icon
    def __init__(self, pos_x, pos_y, width, height, color_or_picture):
        self.rect = pygame.Rect(pos_x, pos_y, width, height)
        self.color_or_picture = color_or_picture
        self.screen_width: int = pygame.display.Info().current_w
        self.screen_height: int = pygame.display.Info().current_h
        self.x = pos_x
        self.y = pos_y
        self.color_or_picture = self.initialize_icon(color_or_picture)

    # checks if icon is tuple or pygame.Surface
    def initialize_icon(self, icon):
        if type(self.color_or_picture) == tuple:
            return icon
        elif type(self.color_or_picture) == pygame.Surface:
            return pygame.transform.scale(icon, (int(self.screen_width / 30), int(self.screen_width / 30)))

    # checks if mouse is over icon
    def check_collide_point(self, mousepos: Tuple[int, int]) -> bool:
        # noinspection PyArgumentList
        if self.rect.collidepoint(mousepos) and pygame.mouse.get_pressed()[0]:
            return True
        return False

    # render of icon
    def draw_rect(self, screen):
        if type(self.color_or_picture) == tuple:
            pygame.draw.rect(screen, self.color_or_picture, self.rect)
        elif type(self.color_or_picture) == pygame.Surface:
            screen.blit(self.color_or_picture, (self.x, self.y))
