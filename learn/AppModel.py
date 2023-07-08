import sys

from PyQt5.QtWidgets import QWidget, QMainWindow, QPushButton, QVBoxLayout, QApplication


class Model:
    pass


class ReactiveModel:
    __attribs = Model()
    __cbs = Model()

    def __init__(self):
        super().__init__()

    def __getattr__(self, attr: str):
        if hasattr(self.__attribs, attr):
            return getattr(self.__attribs, attr)

    def __setattr__(self, attr: str, value):
        print("Yep", attr, value)
        setattr(self.__attribs, attr, value)
        if hasattr(self.__cbs, attr):
            cbs: list = getattr(self.__cbs, attr)
            for cb in cbs:
                cb(value)

    def on_change(self, attrib: str, cb):
        if not hasattr(self.__cbs, attrib):
            setattr(self.__cbs, attrib, [])
        cbs: list = getattr(self.__cbs, attrib)
        cbs.append(cb)


class AppViewModel(ReactiveModel):
    state: str
    expression: str


def update(new_val, old_val):
    print(new_val, old_val)


app_model = AppViewModel()
app_model.expression = ""
app_model.deg = True
app_model.state = "menu"

# спустя время
app_model.complexity = 3
app_model.state = "game"


class MainWindow(QMainWindow):
    __current_view: QWidget

    def __init__(self) -> None:
        super().__init__()
        app_model.on_change("state", lambda state: self.__check_state())
        self.show()

    def __check_state(self):
        if app_model == "menu":
            LevelMenuView(self)
        elif app_model == "game":
            # LevelView(self)
            pass


class LevelMenuView(QWidget):
    def __init__(self, window: QMainWindow) -> None:
        super().__init__()
        window.setCentralWidget(self)
        layout = QVBoxLayout()
        self.setLayout(layout)
        for i in range(1, 4):
            button_index = i
            button = QPushButton(str(i))
            button.click.connect(lambda: self.__on_level_select(button_index))
        app_model.on_change("state", lambda state: self._check_state())

    def _check_state(self):
        if app_model != "menu":
            self.destroy()

    def __on_level_select(lvl: int):
        app_model.complexity = lvl
        app_model.state = "game"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    app.exec()
