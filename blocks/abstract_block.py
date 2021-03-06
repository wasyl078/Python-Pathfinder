# imports
from abc import abstractmethod
from general.consts_values import *


# abstract class for objects contains every important variable for standard block in game
# also contains two abstract methods - update() and render()
class AbtractBlock(object):

    # constructor - defines every variable that will be used in render() and update()
    def __init__(self, posx: int, posy: int, color=Color.RED, block_type: str = Blocks.ABSTRACT, damageable: bool = False):
        self.pos_x = posx
        self.pos_y = posy
        self.block_type = block_type
        self.rows = NUMBER_OF_OF_BLOCKS[1]
        self.columns = NUMBER_OF_OF_BLOCKS[0]
        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h
        self.def_width = self.screen_width / self.columns
        self.def_height = self.screen_height / self.rows
        self.damageable = damageable
        self.color = color
        if type(color) == pygame.Surface:
            self.color = pygame.transform.scale(self.color, (int(self.def_width), int(self.def_height)))

    # this method is supposed to update object's position every clock's tick
    # if necessery - it should be overriden
    @abstractmethod
    def update(self, matrix, moveable_objects):
        pass

    # this method is standard render method - draws square in right place in window or picture
    @abstractmethod
    def render(self, screen: pygame.Surface):
        if type(self.color) == tuple:
            buf_rect = pygame.Rect(self.pos_x * self.def_width, self.pos_y * self.def_height, self.def_width, self.def_height)
            pygame.draw.rect(screen, self.color, buf_rect)
        else:
            screen.blit(self.color, (self.pos_x * self.def_width, self.pos_y * self.def_height))

    # this method supports checking if it is possible to move into particular block
    def check_place(self, posx: int, posy: int, matrix, moveable_objects) -> bool:
        if posx < 0 or posx > self.columns - 1 or posy < 0 or posy > self.rows - 1:
            return False
        if matrix.two_dim_list[posx][posy]:
            for block in moveable_objects:
                if block.pos_x == posx and block.pos_y == posy and self != block and not block:
                    return False
            return True
        return False

    # overwriting hash method - only pos_x, pos_y and block_type matters:
    def __hash__(self):
        return hash((self.pos_x, self.pos_y, self.block_type))

    # overwriting eq method - only pos_x, pos_y and block_type are being checked:
    def __eq__(self, other):
        return self.pos_x == other.pos_x and self.pos_y == other.pos_y and self.block_type == other.block_type

    # overwriting str method - easier to "debug"
    def __str__(self):
        return "{}x{} ({})".format(self.pos_x, self.pos_y, self.block_type)

    # overriding __bool_(self) -> True - you can move there, False -> you can't move there
    @abstractmethod
    def __bool__(self) -> bool:
        return True
