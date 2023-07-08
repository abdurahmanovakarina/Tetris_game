import random

from .L_block import LBlock
from .L_block_2 import LBlock2
from .S_block import SBlock
from .S_block_2 import SBlock2
from .T_block import TBlock
from .line_block import LineBlock
from .square_block import SquareBlock


class BlockFactory:
    @staticmethod
    def get_random_block(x, y):
        """Создает случайно выбранный блок в заданной позиции"""
        r = random.randrange(7)
        if r == 0:
            return SquareBlock(x, y)
        elif r == 1:
            return LineBlock(x, y)
        elif r == 2:
            return TBlock(x, y)
        elif r == 3:
            return LBlock(x, y)
        elif r == 4:
            return LBlock2(x, y)
        elif r == 5:
            return SBlock(x, y)
        elif r == 6:
            return SBlock2(x, y)
        else:
            raise RuntimeError("Wrong block number")

    @staticmethod
    def get_brick_block(x, y):
        return SquareBlock(x, y)
