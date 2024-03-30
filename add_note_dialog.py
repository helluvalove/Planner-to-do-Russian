from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton, QDialogButtonBox, QTextEdit
from PyQt5.QtCore import Qt

class AddNoteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Note")
        self.layout = QVBoxLayout()

        self.firstInputLabel = QLabel("Main Note:")
        self.firstInput = QLineEdit()
        self.layout.addWidget(self.firstInputLabel)
        self.layout.addWidget(self.firstInput)

        self.secondInputLabel = QLabel("Additional Note:")
        self.secondInput = QTextEdit()
        # Установка фиксированной высоты для поля дополнительной записи
        self.secondInput.setFixedHeight(100)  # Замените 100 на желаемую высоту
        # Разрешение только вертикальной полосы прокрутки
        self.secondInput.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.layout.addWidget(self.secondInputLabel)
        self.layout.addWidget(self.secondInput)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

        self.setLayout(self.layout)

    def getInputs(self):
        return self.firstInput.text(), self.secondInput.toPlainText()