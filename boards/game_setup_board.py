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

    def update(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        print(mouse_pos)
        buf_rect = pygame.Rect(1000, 1440 / 2, 560, 300)

        if buf_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.choosen_color = True

    def render(self) -> None:
        self.screen.fill(Color.BLACK)
        img = pygame.image.load("pictures/pathfinder menu v2.png")
        img = pygame.transform.scale(img, (self.screen_width, self.screen_height))
        self.screen.blit(img, (0, 0))

        buf_rect = pygame.Rect(1000, 1440 / 2, 560, 300)
        pygame.draw.rect(self.screen, (100, 100, 100), buf_rect)

        pygame.display.flip()
