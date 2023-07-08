from PyQt5 import uic
from PyQt5.QtWidgets import (
    QDesktopWidget,
    QWidget,
    QMainWindow,
    QAction,
)

from .menu_view import MenuView
from .tetris_view import TetrisView
from .results_view import ResultsView
from ...UI import main_window_ui
from ...utils.commands import ExitCommand, ShowMessageCommand
from ...viewModel.main_view_model import app_model


class MainWindow(QMainWindow):
    """
    Класс MainWindow представляет главное окно приложения.

    Он является подклассом QMainWindow и отвечает за обработку различных представлений и состояний приложения, а также за обработку действий меню и других команд.

    Attributes:
        __current_view (QWidget): The current view being displayed in the main window.

    Methods:
        __init__(self) -> None: Инициализирует главное окно и устанавливает пользовательский интерфейс, действия меню и начальный вид.
        __load_ui(self): Загружает пользовательский интерфейс для главного окна из файла .ui.
        __setup_menu_actions(self): Подключает действия меню к соответствующим командам.
        __center(self): Центрирует главное окно на экране.
        __check_state(self): Изменяет вид, основываясь на текущем состоянии приложения.
        __check_command(self): Выполняет соответствующее действие на основе текущей команды приложения.
    """

    __current_view: QWidget

    def __init__(self) -> None:
        super().__init__()

        app_model.on_change("state", lambda state: self.__check_state())
        app_model.on_change("command", lambda command: self.__check_command())

        self.__load_ui()

        self.__setup_menu_actions()

        self.__current_view = MenuView(self)
        self.setCentralWidget(self.__current_view)

        # self.__center()
        self.show()

    def __load_ui(self):
        """
        Загружает пользовательский интерфейс для главного окна.
        """
        uic.loadUi(main_window_ui, self)
        self.menuExitAction: QAction
        self.menuAboutProgramAction: QAction

    def __setup_menu_actions(self):
        """
        Установка действий меню для главного окна программы.
        """
        self.menuExitAction.triggered.connect(lambda: app_model.set_command("exit"))
        self.menuAboutProgramAction.triggered.connect(
            lambda: app_model.set_command("about_programm")
        )

    # def __center(self):
    #     """
    #     Центрирует главное окно на экране
    #     """
    #     screen = QDesktopWidget().screenGeometry()
    #     size = self.geometry()
    #     self.move(
    #         (screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2
    #     )

    def __check_state(self):
        """
        Проверка и обновление текущего представления на основе текущего состояния приложения.
        """
        if app_model.state == "menu":
            self.__current_view = MenuView(self)
            self.statusBar().showMessage("")
        elif app_model.state == "game":
            self.__current_view = TetrisView(self)
        elif app_model.state == "results":
            self.__current_view = ResultsView(self)

    def __check_command(self):
        """
        Проверка текущей команды в app_model и выполните соответствующего действия.
        """
        if app_model.command == "exit":
            # self.close()
            ExitCommand(self).execute()

        elif app_model.command == "about_programm":
            ShowMessageCommand(
                "Выполнил студент САФУ, 3 курс, 351018."
            ).execute()
