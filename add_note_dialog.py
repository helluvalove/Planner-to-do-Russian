from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton, QDialogButtonBox, QTextEdit
from PyQt5.QtCore import Qt

class AddNoteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавление записи")
        self.layout = QVBoxLayout()

        self.firstInputLabel = QLabel("Заголовок:")
        self.firstInput = QLineEdit()
        self.layout.addWidget(self.firstInputLabel)
        self.layout.addWidget(self.firstInput)

        self.secondInputLabel = QLabel("Запись:")
        self.secondInput = QTextEdit()
        # Установка фиксированной высоты для поля дополнительной записи
        self.secondInput.setFixedHeight(190)  # Замените 100 на желаемую высоту
        # Разрешение только вертикальной полосы прокрутки
        self.secondInput.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.layout.addWidget(self.secondInputLabel)
        self.layout.addWidget(self.secondInput)

        self.buttons = QDialogButtonBox()
        self.ok_button = self.buttons.addButton("Ок", QDialogButtonBox.AcceptRole)
        self.cancel_button = self.buttons.addButton("Отмена", QDialogButtonBox.RejectRole)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)
        
        self.setLayout(self.layout)
        self.adjustSize()  # Автоматически рассчитываем размеры на основе содержимого
        self.setMinimumSize(self.size())  # Устанавливаем минимальный размер окна

    def getInputs(self):
        return self.firstInput.text(), self.secondInput.toPlainText()