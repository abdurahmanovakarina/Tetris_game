from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton

from ...UI import menu_view_ui
from ...utils.commands import GetRecordCommand, GetLastScoreCommand
from ...viewModel.main_view_model import app_model


class MenuView(QWidget):
    """
    Класс виджета, представляющий вид меню игры "Тетрис".

    Attributes:
        main_window (QMainWindow): Главное окно приложения.
        recordsLabel (QLabel): Label, отображающий рекорды и последние результаты для каждого уровня.
        toTetris1ViewButton (QPushButton): Кнопка, ведущая на первый уровень игры.
        toTetris2ViewButton (QPushButton): Кнопка, ведущая на второй уровень игры.
        toTetris3ViewButton (QPushButton): Кнопка, ведущая на третий уровень игры.
    """

    def __init__(self, main_window) -> None:
        """
        Инициализирует виджет представления меню.

        Args:
            main_window (QMainWindow): Главное окно приложения.
        """
        super().__init__()
        self.main_window = main_window
        self.main_window.setCentralWidget(self)
        uic.loadUi(menu_view_ui, self)
        self.__setup_buttons()

        self.recordsLabel: QLabel
        self.recordsLabel.setText(
            f"1 уровень\nрекорд: {GetRecordCommand(1).execute()}, последний счёт: {GetLastScoreCommand(1).execute()}\n\n2 уровень\nрекорд: {GetRecordCommand(2).execute()}, последний счёт: {GetLastScoreCommand(2).execute()}\n\n3 уровень\nрекорд: {GetRecordCommand(3).execute()}, последний счёт: {GetLastScoreCommand(3).execute()}"
        )

    def __setup_buttons(self):
        """
        Устанавливает кнопки представления меню.
        """
        self.toTetris1ViewButton: QPushButton
        self.toTetris1ViewButton.clicked.connect(lambda: app_model.set_complexity(1))
        self.toTetris1ViewButton.clicked.connect(lambda: app_model.set_state("game"))

        self.toTetris2ViewButton: QPushButton
        self.toTetris2ViewButton.clicked.connect(lambda: app_model.set_complexity(2))
        self.toTetris2ViewButton.clicked.connect(lambda: app_model.set_state("game"))

        self.toTetris3ViewButton: QPushButton
        self.toTetris3ViewButton.clicked.connect(lambda: app_model.set_complexity(3))
        self.toTetris3ViewButton.clicked.connect(lambda: app_model.set_state("game"))
