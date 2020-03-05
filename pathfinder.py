# imports
import ctypes
from boards.game_board import Game
from boards.game_setup_board import GameSetup


# avoiding display scalling by windows "maku UI larger or smaller"
ctypes.windll.user32.SetProcessDPIAware()

# starting game:
if __name__ == "__main__":
    actual = GameSetup()
    color = actual.game_setup_loop()
    actual_game = Game()
    actual_game.game_loop(actual_game)
