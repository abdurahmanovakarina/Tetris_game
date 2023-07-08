from .brick import Brick


class SBlock(Brick):
    def __init__(self, x, y):
        # rotation pos: 1: горизонтальное, 2: вертикальное
        self.rotation_pos = 1
        super().__init__(x, y)

    def get_name(self):
        return "SBlock"

    def get_arm_direction(self):
        """Эта функция контролирует, является ли блок левым или правым зеркальным отображением"""
        return 1

    def get_coords(self):
        x = self.get_x()
        y = self.get_y()
        if self.rotation_pos == 1:
            return [
                (x, y),
                (x + self.get_arm_direction(), y),
                (x, y + 1),
                (x - self.get_arm_direction(), y + 1),
            ]
        else:
            return [
                (x, y),
                (x - 1, y),
                (x - 1, y - self.get_arm_direction()),
                (x, y + self.get_arm_direction()),
            ]

    def rotate_left(self):
        if self.rotation_pos == 1:
            self.rotation_pos = 2
        else:
            self.rotation_pos = 1

    def rotate_right(self):
        self.rotate_left()
