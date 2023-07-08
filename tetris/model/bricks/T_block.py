from .brick import Brick


class TBlock(Brick):
    def __init__(self, x, y):
        # rotation pos: 1: вниз, 2: влево, 3: вверх, 4: вправо
        self.rotation_pos = 1
        super().__init__(x, y)

    def get_name(self):
        return "TBlock"

    def get_coords(self):
        x = self.get_x()
        y = self.get_y()
        if self.rotation_pos == 1:
            return [(x - 1, y), (x, y), (x + 1, y), (x, y + 1)]
        elif self.rotation_pos == 2:
            return [(x, y - 1), (x, y), (x, y + 1), (x - 1, y)]
        elif self.rotation_pos == 3:
            return [(x - 1, y), (x, y), (x + 1, y), (x, y - 1)]
        elif self.rotation_pos == 4:
            return [(x, y - 1), (x, y), (x, y + 1), (x + 1, y)]

    def rotate_left(self):
        if self.rotation_pos == 1:
            self.rotation_pos = 4
        else:
            self.rotation_pos = self.rotation_pos - 1

    def rotate_right(self):
        if self.rotation_pos == 4:
            self.rotation_pos = 1
        else:
            self.rotation_pos = self.rotation_pos + 1
