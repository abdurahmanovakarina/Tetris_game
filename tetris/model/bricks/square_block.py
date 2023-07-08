from .brick import Brick


class SquareBlock(Brick):
    def __init__(self, x, y):
        super().__init__(x, y)

    def get_name(self):
        return "SquareBlock"

    def get_coords(self):
        x = self.get_x()
        y = self.get_y()
        return [(x, y), (x + 1, y + 1), (x, y + 1), (x + 1, y)]
