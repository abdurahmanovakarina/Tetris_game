from .brick import Brick


class LBlock(Brick):
    def __init__(self, x, y):
        # rotation pos: 1: вправо, 2: вниз, 3: влево, 4: вверх
        self.rotation_pos = 1
        super().__init__(x, y)

    def get_name(self):
        return "LBlock"

    def get_arm_direction(self):
        """Эта функция контролирует, является ли блок левым или правым зеркальным отображением"""
        return 1

    def get_coords(self):
        x = self.get_x()
        y = self.get_y()
        if self.rotation_pos == 1:
            return [
                (x, y - 1),
                (x, y),
                (x, y + 1),
                (x + self.get_arm_direction(), y + self.get_arm_direction()),
            ]
        elif self.rotation_pos == 2:
            return [
                (x - 1, y),
                (x, y),
                (x + 1, y),
                (x - 1, y + self.get_arm_direction()),
            ]
        elif self.rotation_pos == 3:
            return [
                (x - self.get_arm_direction(), y - 1),
                (x, y - 1),
                (x, y),
                (x, y + 1),
            ]
        elif self.rotation_pos == 4:
            return [
                (x - 1, y),
                (x, y),
                (x + 1, y),
                (x + 1, y - self.get_arm_direction()),
            ]

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
