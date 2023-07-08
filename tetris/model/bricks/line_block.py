from .brick import Brick


class LineBlock(Brick):
    def __init__(self, x, y):
        # rotation pos: 1: горизонтальное, 2: вертикальное
        self.rotation_pos = 1
        super().__init__(x, y)

    def get_name(self):
        return "LineBlock"

    def get_coords(self):
        x = self.get_x()
        y = self.get_y()
        if self.rotation_pos == 1:
            return [(x - 1, y), (x, y), (x + 1, y), (x + 2, y)]
        else:
            return [(x, y - 1), (x, y), (x, y + 1), (x, y + 2)]

    def rotate_left(self):
        if self.rotation_pos == 1:
            self.rotation_pos = 2
        else:
            self.rotation_pos = 1

    def rotate_right(self):
        self.rotate_left()
