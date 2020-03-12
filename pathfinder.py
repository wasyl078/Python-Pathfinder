# imports
import ctypes
from boards.game_board import Game
from boards.game_setup_board import GameSetup
import platform

# avoiding display scalling by windows "maku UI larger or smaller"
if platform.system() == 'Windows':
    ctypes.windll.user32.SetProcessDPIAware()

# starting game:
if __name__ == "__main__":
    actual_game = GameSetup()
    color_or_png = actual_game.game_setup_loop()
    actual_game = Game(color_or_png)
    actual_game.game_loop(actual_game, color_or_png)


# TODO enemy's AI
# TODO local multiplayer
# TODO special blocks
# TODO new players pictures
# TODO boards (game engine) refactor (as queue)
# TODO code refactor (e.x generator: for + if, comments, type hints)
# TODO over network multiplayer
