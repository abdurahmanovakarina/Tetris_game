from typing import Tuple


class Brick:
    def __init__(self, x: int, y: int):
        """Инициализация блока в заданной позиции на экране"""
        self.__xPos = 0
        self.__yPos = 0
        self.set_pos(x, y)

    def set_pos(self, x, y):
        self.__xPos = x
        self.__yPos = y

    def get_pos(self):
        return int(self.x), int(self.y)

    def move_down(self):
        self.set_pos(self.get_x(), self.get_y() + 1)

    def move_left(self):
        self.set_pos(self.get_x() - 1, self.get_y())

    def move_right(self):
        self.set_pos(self.get_x() + 1, self.get_y())

    def get_x(self):
        return int(self.__xPos)

    def get_y(self):
        return int(self.__yPos)

    def rotate_left(self):
        pass

    def rotate_right(self):
        pass

    def get_coords(self) -> Tuple[int, int]:
        """Возвращает все точки"""
        pass

    def peek_coords(self, x_offset, y_offset):
        """Возвращает все точки, имитируя движение блока, без фактического обновления координат"""
        coords = self.get_coords()  # массив пар
        return list(map(lambda pt: (pt[0] + x_offset, pt[1] + y_offset), coords))

    def peek_rotated_coords(self, direction):
        """Получает координаты после вращения, не применяя их постоянно
        Направление: 1: право, -1: лево
        """
        if direction == 1:
            self.rotate_right()
        else:
            self.rotate_left()
        coords = self.get_coords()
        if direction == 1:
            self.rotate_left()
        else:
            self.rotate_right()
        return coords

    def get_name(self):
        return
