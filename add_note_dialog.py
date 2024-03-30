from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton, QDialogButtonBox

class AddNoteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Add event")
        
        layout = QVBoxLayout(self)
        
        # Добавляем первое поле ввода
        self.firstInput = QLineEdit(self)
        layout.addWidget(QLabel("Event:"))
        layout.addWidget(self.firstInput)
        
        # Добавляем второе поле ввода
        self.secondInput = QLineEdit(self)
        layout.addWidget(QLabel("Additional Note:"))
        layout.addWidget(self.secondInput)
        
        # Добавляем кнопки OK и Cancel
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        layout.addWidget(self.buttons)
        
        self.buttons.accepted.connect(self.onAccepted)
        self.buttons.rejected.connect(self.reject)

    def getInputs(self):
        return self.firstInput.text(), self.secondInput.text()

    def onAccepted(self):
        # Метод, вызываемый при нажатии на OK
        self.accept()