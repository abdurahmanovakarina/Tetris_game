import sys
from PyQt5.QtWidgets import QApplication
from .view.mainWindow.main_window import MainWindow

# from rich.traceback import install
# install(show_locals=True)

app = QApplication(sys.argv)
sys.path.append(".")
sys.path.append("./tetris")

main_window = MainWindow()
app.exec()
sys.exit()
