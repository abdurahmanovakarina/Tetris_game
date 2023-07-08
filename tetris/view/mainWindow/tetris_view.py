from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QVBoxLayout

from .Board import Board
from .Game import Game
from ...UI import tetris_view_ui
from ...viewModel.main_view_model import app_model


class TetrisView(QWidget):
    """
    Виджет для отображения игры Тетрис.

    Этот класс является подклассом QWidget и используется для отображения игры Тетрис.
    Он включает методы для настройки пользовательского интерфейса, рисования игрового поля,
    обновления строки состояния и обработки клавиатурного ввода от пользователя.
    """

    BrickSize: int = 15
    Margin = 50

    def __init__(self, main_window) -> None:
        super().__init__()
        self.pauseButton = None
        self.toMenuViewButton = None
        self.verticalLayout = None
        self.__scene = None
        self.__lvl = app_model.complexity
        self.main_window = main_window
        self.__status_bar = self.main_window.statusBar()

        self.main_window.setCentralWidget(self)
        uic.loadUi(tetris_view_ui, self)

        self.__board = Board(self.__lvl)
        self.__game = Game(self.__board)
        self.initialize_ui()
        self.__game.start()
        self.__setup_buttons()

    def initialize_ui(self):
        """
        Устанавливает пользовательский интерфейс для игры Тетрис.

        Этот метод создает виджет QGraphicsView и QGraphicsScene, и устанавливает
        сцену в качестве центрального виджета главного окна. Он также устанавливает размер
        сцены равным размеру игрового поля и добавляет светло-серый фон сцены.
        """
        qgv = QGraphicsView(self)
        self.__scene = QGraphicsScene(qgv)
        qgv.setScene(self.__scene)
        self.verticalLayout: QVBoxLayout
        self.verticalLayout.addWidget(qgv)

        # self.main_window.resize(
        #     self.__board.width * self.BrickSize + self.Margin,
        #     (self.__board.height + 5) * self.BrickSize + self.Margin,
        # )

        self.__scene.setSceneRect(
            0,
            0,
            self.__board.width * self.BrickSize,
            self.__board.height * self.BrickSize,
        )

        self.draw_board()

        self.__game.board_updated.connect(self.draw_board)
        self.__game.score_updated.connect(self.update_status)
        self.__game.level_updated.connect(self.update_status)
        self.__game.status_updated.connect(self.update_status)

        self.update_status()

    def draw_board(self):
        """
        Рисует текущее состояние игры Тетрис на сцене QGraphicsScene.

        Этот метод сначала очищает сцену, а затем добавляет на сцену
        прямоугольники, представляющие текущий блок, препятствия
        и любые заполненные клетки на игровой доске.
        """
        self.__scene.clear()
        self.__scene.addRect(self.__scene.sceneRect(), QPen(Qt.lightGray))
        for point in self.__board.current_block.get_coords():
            self.__scene.addRect(
                point[0] * self.BrickSize,
                point[1] * self.BrickSize,
                self.BrickSize,
                self.BrickSize,
            )
        for obstacle in self.__board.obstacles:
            for point in obstacle.get_coords():
                self.__scene.addRect(
                    point[0] * self.BrickSize,
                    point[1] * self.BrickSize,
                    self.BrickSize,
                    self.BrickSize,
                    QPen(Qt.lightGray),
                    QBrush(Qt.black),
                )

        for i in range(0, self.__board.width):
            for j in range(0, self.__board.height):
                if self.__board.data[j][i] != 0:
                    self.__scene.addRect(
                        i * self.BrickSize,
                        j * self.BrickSize,
                        self.BrickSize,
                        self.BrickSize,
                        QPen(Qt.lightGray),
                        QBrush(Qt.green),
                    )

    def update_status(self):
        """
        Обновление строки состояния главного окна для отображения текущего состояния игры.

        Этот метод обновляет строку состояния, чтобы показать текущее состояние игры и счёт.
        """

        self.__status_bar.showMessage(
            "{} Score: {}".format(
                self.__game.get_status(),
                self.__game.get_score(),
                self.__game.get_level(),
            )
        )

    def keyPressEvent(self, e):
        """
        Обработка клавиатурного ввода от пользователя.

        Этот метод проверяет нажатие определенных клавиш (W, A, S, D и Space) и выполняет
        действия в игре на основе нажатой клавиши. Например, если нажата клавиша W,
        то будет предпринята попытка повернуть текущий блок против часовой стрелки.
        Если нажата клавиша "Пробел", то текущий блок ускоряется.

        Args:
            e: Экземпляр QKeyEvent, содержащий информацию о событии нажатия клавиши.
        """
        key = e.key()
        if key == Qt.Key_W:
            if self.__board.can_rotate_current_block(-1):
                self.__board.current_block.rotate_left()
        elif key == Qt.Key_S:
            if self.__board.can_rotate_current_block(1):
                self.__board.current_block.rotate_right()
        elif key == Qt.Key_A:
            if self.__board.can_move_current_block(-1, 0):
                self.__board.current_block.move_left()
        elif key == Qt.Key_D:
            if self.__board.can_move_current_block(1, 0):
                self.__board.current_block.move_right()
        elif key == Qt.Key_Space:
            self.__game.set_high_speed()
        elif key == Qt.Key_N:
            self.__game.new_game()
            self.__game.start()

    def keyReleaseEvent(self, e):
        """
        Обработка клавиатурного ввода от пользователя при отпускании клавиши.

        Args:
            e: Экземпляр QKeyEvent, содержащий информацию о событии отпускания клавиши.
        """
        self.__game.unset_high_speed()

    def __setup_buttons(self) -> None:
        """
        Настройка кнопок в представлении игры Tetris.
        """
        self.toMenuViewButton.clicked.connect(lambda: app_model.set_state("menu"))
        self.pauseButton.clicked.connect(lambda: self.__game.toggle_pause())
