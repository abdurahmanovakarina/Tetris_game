from PyQt5.QtCore import QBasicTimer, pyqtSignal, QObject

from tetris.utils.commands import ShowMessageCommand, SaveScoreCommand
from tetris.view.mainWindow.Board import Board
from tetris.viewModel.main_view_model import app_model


class Game(QObject):
    """
    QObject, представляющий логику игры.
    Выдает сигналы при обновлении поля, счета, уровня или статуса.
    """

    # must be static
    board_updated = pyqtSignal()
    status_updated = pyqtSignal(str)
    score_updated = pyqtSignal(int)
    level_updated = pyqtSignal(int)

    points_for_single_block = 20
    points_for_row_cleared = 100
    points_for_level_up = 400  # после получения n очков ** уровня, уровень повышается
    base_speed = 320  # интервал обновления для уровня 1
    speed_decrement = 20  # декремент таймера для каждого уровня
    high_speed = 50  # интервал таймера при нажатии пробела

    def __init__(self, board: Board):
        super().__init__()
        self.__board = board
        self.__timer = QBasicTimer()
        self.__speed = self.base_speed
        self.__speedBackup = self.__speed
        self.__highSpeedMode = False
        self.__score = 0
        self.__level = 1
        self.__status = ""
        self.__game_over = False
        self.new_game()

    def start(self):
        """
        Запуск игрового таймера.
        """
        if not self.__game_over:
            self.__timer.start(self.__speed, self)

    def stop(self):
        """
        Остановка игрового таймера.
        """
        self.__timer.stop()

    def __change_speed(self, speed):
        """
        Изменение скорости игрового таймера.

        Parameters:
            speed (int): Новая скорость для таймера, в миллисекундах.
        """
        self.__speed = speed
        if self.__timer.isActive():
            self.start()

    def __add_points(self, added):
        """Обновляет очки и скорость.
        Количество добавленных очков зависит от уровня"""
        added = added * self.__level
        self.__score = self.__score + added
        self.score_updated.emit(self.__score)
        self.unset_high_speed()
        if (
            self.__score > self.__number_of_points_to_change_level()
            and self.__speed - self.speed_decrement > 0
        ):
            self.__level = self.__level + 1
            self.level_updated.emit(self.__level)
            self.__change_speed(self.__speed - self.speed_decrement)

    def __number_of_points_to_change_level(self) -> int:
        """
        Расчёт количества очков, необходимого для перехода на следующий уровень.

        Returns:
            Количество очков, необходимое для перехода на следующий уровень.
        """
        return self.points_for_level_up**self.__level

    def __change_status_message(self, msg) -> None:
        """
        Обновление сообщения о статусе игры.

        Parameters:
            msg (str): Новое сообщение о статусе игры для установки.
        """
        self.__status = msg
        self.status_updated.emit(msg)

    def __game_stop(self) -> None:
        """
        Останавливает игру и меняет __game_over на True.

        Этот метод также останавливает таймер и меняет статус на "Game over!".
        Он также сохраняет текущий счет в базе данных и обновляет состояние модели приложения.
        """
        self.__game_over = True
        self.stop()
        self.__change_status_message("Game over!")
        SaveScoreCommand(self.__score, app_model.complexity).execute()
        app_model.state = "results"

    def timerEvent(self, event) -> None:
        """
        Обрабатывает события таймера. Этот метод вызывается фреймворком QT через регулярные промежутки времени
        когда таймер активен.

        Args:
            event: Событие таймера.

        Returns:
            None.
        """
        if event.timerId() == self.__timer.timerId():
            if self.__board.is_current_block_on_obstacle(0, 1):
                self.__game_stop()
            elif self.__board.can_move_current_block(0, 1):
                self.__board.current_block.move_down()
            else:
                self.__board.permanently_insert_current_block()
                self.__add_points(self.points_for_single_block)
                rows_removed = self.__board.remove_full_rows()
                self.__add_points(self.points_for_row_cleared * rows_removed)
                if not self.__board.try_insert_random_block():
                    self.__game_stop()
            self.board_updated.emit()

    def get_status(self) -> str:
        """
        Возвращает сообщение о текущем состоянии игры.

        Returns:
            Сообщение о текущем состоянии игры.
        """
        return self.__status

    def get_score(self) -> int:
        """
        Возвращает текущий счет игры.

        Returns:
            Текущий счет игры.
        """
        return self.__score

    def get_level(self) -> int:
        """
        Возвращает текущий уровень игры.

        Returns:
            Текущий уровень игры.
        """
        return self.__level

    def set_high_speed(self):
        """
        Установка таймера игры на высокоскоростной интервал.
        """
        if not self.__highSpeedMode:
            self.__highSpeedMode = True
            self.__speedBackup = self.__speed
            self.__change_speed(self.high_speed)

    def unset_high_speed(self):
        """
        Установка таймераа игры обратно на нормальный интервал скорости.
        """
        if self.__highSpeedMode:
            self.__change_speed(self.__speedBackup)
            self.__highSpeedMode = False

    def toggle_pause(self):
        """
        Переключает состояние паузы в игре.

        Если игра в данный момент приостановлена, она будет возобновлена.
        Если игра запущена, она будет приостановлена.
        """
        if not self.__game_over:
            if self.__timer.isActive():
                self.__change_status_message("Paused")
                self.stop()
            else:
                self.start()
                self.__change_status_message("")

    def new_game(self):
        """
        Начать новую игру.

        Метод обнулит состояние игры, включая счет, уровень и сообщение о состоянии, и вставит новый случайный блок на поле.
        """
        self.stop()
        self.__speed = self.base_speed
        self.__speedBackup = self.__speed
        self.__highSpeedMode = False
        self.__score = 0
        self.__level = 1
        self.__game_over = False
        self.score_updated.emit(self.__score)
        self.level_updated.emit(self.__level)
        self.__change_status_message("")
        self.__board.remove_all()
        self.__board.insert_obstacles()
        self.__board.try_insert_random_block()
        self.board_updated.emit()
