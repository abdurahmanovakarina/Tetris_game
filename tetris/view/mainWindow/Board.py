from ...model.bricks import brick
from ...utils.commands import GetRandomBlockCommand, GetSquareBlockCommand
from ...viewModel.main_view_model import app_model


class Board:
    """Класс, представляющий доску для игры Тетрис.

    Атрибуты:
        current_block (brick.Brick): текущий блок.
        width (int): ширина доски.
        height (int): высота доски.
        new_block_x (float): начальная позиция нового блока по оси x.
        new_block_y (float): начальная позиция нового блока по оси y.

    """

    current_block = ...  # type: brick.Brick
    width: int
    height: int

    new_block_x: float
    new_block_y: float

    def __init__(self, lvl):
        """
        Инициализирует доску с указанным уровнем сложности.

        Args:
            lvl (int): Уровень сложности, который определяет размер доски.
        """
        if lvl == 1:
            self.width = 10
            self.height = 20
        elif lvl == 2:
            self.width = 20
            self.height = 30
        elif lvl == 3:
            self.width = 30
            self.height = 40

        self.new_block_x = self.width / 2 - 1
        self.new_block_y = 0

        self.data = [[0] * self.width for _ in range(self.height)]
        self.data_obstacles = [[0] * self.width for _ in range(self.height)]
        self.current_block = None

    def insert_obstacles(self) -> bool:
        """
        Добавляет препятствия на доску в зависимости от уровня сложности.
        """
        self.obstacles = []
        if app_model.complexity == 1:
            pass
        elif app_model.complexity == 2:
            self.insert_obstacle(0, int(self.height / 2 - 1))
        elif app_model.complexity == 3:
            self.insert_obstacle(0, int(self.height / 2 - 1))
            self.insert_obstacle(self.width / 1.3 - 1, self.height / 2.7 - 1)

    def insert_obstacle(self, obstacle_x, obstacle_y):
        """
        Добавляет одно препятствие на доску в указанной позиции.

        Args:
            obstacle_x (float): Координата x для добавления препятствия.
            obstacle_y (float): Координата y для добавления препятствия.
        Returns:
            bool: Возвращает True, если препятствие было успешно добавлено.
        """
        self.obstacles.append(GetSquareBlockCommand(obstacle_x, obstacle_y).execute())

        for obstacle in self.obstacles:
            for pt in obstacle.get_coords():
                self.data_obstacles[pt[1]][pt[0]] = 1

            print("Inserted ", obstacle.get_name())
        return True

    def is_current_block_on_obstacle(self, x_offset, y_offset) -> bool:
        """
        Проверяет, находится ли текущий блок на препятствии.

        Args:
            x_offset (int): Смещение по оси x.
            y_offset (int): Смещение по оси y.

        Returns:
            bool: Возвращает True, если текущий блок находится на препятствии, иначе False.
        """
        coords = self.current_block.peek_coords(x_offset, y_offset)
        for x, y in coords:
            try:
                if self.data_obstacles[y][x] == 1:
                    return True
            except IndexError:
                pass

    def try_insert_random_block(self):
        """
        Пытается вставить случайный блок на доску.
        Если успешно, то устанавливает сгенерированный блок в качестве текущего.

        Returns:
            bool: Возвращает True, если блок был успешно вставлен, иначе False.
        """
        self.current_block = GetRandomBlockCommand(
            self.new_block_x, self.new_block_y
        ).execute()

        for pt in self.current_block.get_coords():
            if (
                pt[0] >= 0 and pt[1] >= 0
            ):  # блоки могут быть созданы в отрицательном положении
                if self.data[pt[1]][pt[0]] != 0:
                    return False

        print("Inserted ", self.current_block.get_name())
        return True

    def can_move_current_block(self, x_offset, y_offset):
        """
        Проверяет, может ли текущий блок быть смещен в указанную позицию.

        Args:
            x_offset (int): Смещение по оси x.
            y_offset (int): Смещение по оси y.

        Returns:
            bool: Возвращает True, если текущий блок может быть смещен, иначе False.
        """
        coords = self.current_block.peek_coords(x_offset, y_offset)
        return all(
            0 <= x < self.width and 0 <= y < self.height for x, y in coords
        ) and all(self.data[j][i] == 0 for i, j in coords)

    def can_rotate_current_block(self, direction):
        """
        Проверяет, может ли текущий блок быть повернут в указанную сторону.

        Args:
            direction (int): Направление, в которое нужно повернуть блок (1 - направо, 2 - налево).

        Returns:
            bool: Возвращает True, если текущий блок может быть повернут, иначе False.
        """
        coords = self.current_block.peek_rotated_coords(direction)
        return all(
            0 <= x < self.width and 0 <= y < self.height for x, y in coords
        ) and all(self.data[j][i] == 0 for i, j in coords)

    def permanently_insert_current_block(self):
        """
        Перманентно вставляет текущий блок на доску.
        """
        for pt in self.current_block.get_coords():
            self.data[pt[1]][pt[0]] = 1

    def remove_full_rows(self) -> int:
        """
        Удаляет заполненные линии из доски.

        Возвращает количество удаленных строк (0, если они any).
        """
        rows_removed = 0
        for row in range(0, self.height):
            if all(self.data[row][col] for col in range(0, self.width)):
                rows_removed = rows_removed + 1
                for row1 in range(row, 0, -1):  # y axis goes down
                    self.__copy_row(row1 - 1, row1)
                self.__clear_row(0)
        return rows_removed

    def remove_all(self) -> None:
        """
        Удаляет все данные и препятствия с доски.

        Returns:
            None.
        """
        for row in range(0, self.height):
            for col in range(0, self.width):
                self.data[row][col] = 0

    def __copy_row(self, src_row_index, target_row_index) -> None:
        """
        Копирует значения данных в заданной исходной строке в заданную целевую строку.

        Args:
            source_row_idx (int): Индекс исходной строки для копирования данных.
            target_row_idx (int): Индекс целевой строки для копирования данных.

        Returns:
            None.
        """
        for i in range(0, self.width):
            self.data[target_row_index][i] = self.data[src_row_index][i]

    def __clear_row(self, row_index) -> None:
        """
        Очищает данные в заданной строке.

        Args:
            row_idx (int): Индекс строки, которую нужно очистить.

        Returns:
            None.
        """
        for i in range(0, self.width):
            self.data[row_index][i] = 0
