import pygame
from general.consts_values import Color
import sys


class GameSetup(object):
    def __init__(self) -> None:
        self.tps_max = 30.0
        self.choosen_color = None
        self.tps_clock = pygame.time.Clock()
        self.tps_delta = 0.0
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width: int = pygame.display.Info().current_w
        self.screen_height: int = pygame.display.Info().current_h
        self.color_rectangles = list()
        self.initialize_color_rectangles()

    def game_setup_loop(self) -> str:
        while self.choosen_color is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    sys.exit()

            self.tps_delta += self.tps_clock.tick() / 1000.0
            while self.tps_delta > 1 / self.tps_max:
                self.update()
                self.tps_delta -= 1 / self.tps_max
            self.render()
        return self.choosen_color

    def initialize_color_rectangles(self):
        x = self.screen_width / 5
        y = self.screen_height * 5 / 10
        def_side = self.screen_width / 30
        for color in Color.playable_colors_list:
            buf_rect = ColorRectangle(x, y, def_side, def_side, color)
            self.color_rectangles.append(buf_rect)
            x += self.screen_width / 5
            if x == self.screen_width:
                x = self.screen_width / 5
                y += self.screen_height / 10

    def update(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        for color_rect in self.color_rectangles:
            if color_rect.check_collide_point(mouse_pos):
                self.choosen_color = color_rect.color_or_picture

    def render(self) -> None:
        self.screen.fill(Color.BLACK)
        img = pygame.image.load("pictures/pathfinder menu v2.png")
        img = pygame.transform.scale(img, (self.screen_width, self.screen_height))
        self.screen.blit(img, (0, 0))

        for color_rect in self.color_rectangles:
            color_rect.draw_rect(self.screen)

        pygame.display.flip()


class ColorRectangle(object):
    def __init__(self, pos_x, pos_y, width, height, color_or_picture):
        self.rect = pygame.Rect(pos_x, pos_y, width, height)
        self.color_or_picture = color_or_picture
        self.screen_width: int = pygame.display.Info().current_w
        self.screen_height: int = pygame.display.Info().current_h
        self.x = pos_x
        self.y = pos_y
        if type(self.color_or_picture) == tuple:
            self.color_or_picture = color_or_picture
        elif type(self.color_or_picture) == pygame.Surface:
            self.color_or_picture = pygame.transform.scale(self.color_or_picture,
                                                           (int(self.screen_width / 30), int(self.screen_width / 30)))

    def check_collide_point(self, mousepos):
        # noinspection PyArgumentList
        if self.rect.collidepoint(mousepos) and pygame.mouse.get_pressed()[0]:
            return True
        return False

    def draw_rect(self, screen):
        if type(self.color_or_picture) == tuple:
            pygame.draw.rect(screen, self.color_or_picture, self.rect)
        elif type(self.color_or_picture) == pygame.Surface:
            screen.blit(self.color_or_picture, (self.x, self.y))
