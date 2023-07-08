from PyQt5.QtWidgets import QWidget, QLabel, QPushButton
from PyQt5 import uic
from ...UI import results_view
from ...viewModel.main_view_model import app_model
from ...utils.commands import GetRecordCommand, GetLastScoreCommand


class ResultsView(QWidget):
    __current_score: int
    __record_score: int

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.main_window.setCentralWidget(self)
        uic.loadUi(results_view, self)
        self.__get_scores()
        self.__setup_labels()
        self.__setup_buttons()

    def __get_scores(self):
        """
        Получение текущего и рекордного счета в игре.

        Текущий счет извлекается с помощью класса `GetLastScoreCommand`,
        а рекордный счет извлекается с помощью класса `GetRecordCommand`.
        Обоим классам в качестве аргумента передается уровень сложности игры.
        """
        self.__current_score = GetLastScoreCommand(app_model.complexity).execute()
        self.__record_score = GetRecordCommand(app_model.complexity).execute()

    def __setup_labels(self):
        """
        Устанавливает текст виджета `resultsLabel` на основе текущего и рекордного счета.

        Если текущий счет меньше рекордного, то текст виджета `resultsLabel`
        отображает текущий счет и разницу между текущим счетом и рекордным.

        Если текущий счет больше или равен рекордному, то текст `resultsLabel`
        отображает текущий счет и сообщение о том, что был установлен новый рекорд.
        """
        self.resultsLabel: QLabel
        if self.__current_score < self.__record_score:
            self.resultsLabel.setText(
                f"Вы набрали {self.__current_score} очков.\nДо рекорда {self.__record_score} вам не хватило {self.__record_score - self.__current_score} очков."
            )
        else:
            self.resultsLabel.setText(
                f"Новый рекорд!\nВы набрали {self.__current_score} очков!"
            )

    def __setup_buttons(self):
        """
        Настройка кнопок `toMenuViewButton` и `restartButton`.

        Кнопка `toMenuViewButton` связана с методом `set_state` объекта `app_model`, устанавливает состояние приложения на "menu".

        Кнопка `restartButton` аналогично подключена к методу `set_state`, но устанавливает состояние приложения на "game".
        """

        self.toMenuViewButton: QPushButton
        self.toMenuViewButton.clicked.connect(lambda: app_model.set_state("menu"))

        self.restartButton: QPushButton
        self.restartButton.clicked.connect(lambda: app_model.set_state("game"))
