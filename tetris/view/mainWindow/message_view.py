from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QDialog, QPushButton, QLabel

from ...UI import message_view_ui


class MessageView(QDialog):
    """
    Диалоговое окно с ярлыком сообщения и кнопкой подтверждения.

    Attributes:
        __confirm_button (QPushButton): Кнопка подтверждения.
        __message_label (QLabel): Ярлык сообщения.

    """

    __confirm_button: QPushButton
    __message_label: QLabel

    def __init__(self, label_text=None):
        super().__init__()
        uic.loadUi(message_view_ui, self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

        self.messageLabel.setText(label_text)
        self.confirmButton.clicked.connect(lambda: self.close())
