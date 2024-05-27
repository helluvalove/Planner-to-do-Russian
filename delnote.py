import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QPushButton

class HighlightButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMouseTracking(True)
        
        # Устанавливаем стили для обычного состояния кнопки
        self.setStyleSheet("QPushButton {\n"
                            "background-color: #F4DF96;\n"
                            "border-radius: 15%;\n"
                            "border: 1px solid gray;\n"
                            "}\n"
                            "QPushButton:hover {\n"
                            "background-color: #dbb44b;\n"
                            "}")
        
class Ui_DelNote(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(350, 112)
        Dialog.setStyleSheet("#Dialog {\n"
"background-color: #FCF1C9;\n"
"}")
        font = QtGui.QFont("Bahnschrift", 15)
        button_font = QtGui.QFont("Bahnschrift", 13)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(43, 20, 401, 31))
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton = HighlightButton(Dialog)
        self.pushButton.setFont(button_font)
        self.pushButton.setGeometry(QtCore.QRect(180, 60, 71, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(Dialog.reject)
        self.pushButton_2 = HighlightButton(Dialog)
        self.pushButton_2.setFont(button_font)
        self.pushButton_2.setGeometry(QtCore.QRect(260, 60, 71, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(Dialog.accept)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Удаление заметки"))
        Dialog.setFixedSize(350,112)
        self.label.setText(_translate("Dialog", "Вы точно хотите удалить эту запись?"))
        self.pushButton.setText(_translate("Dialog", "Нет"))
        self.pushButton_2.setText(_translate("Dialog", "Да"))

    def enterEvent(self, event):
        # Устанавливаем стили для состояния наведения
        self.setStyleSheet("#pushButton:hover, #pushButton_2:hover {\n"
                        "background-color: #dbb44b;\n"
                        "}"
                        "#pushButton {\n"
                        "background-color: #F4DF96;\n"
                        "border-radius:15%;\n"
                        "border: 1px solid gray;\n"
                        "}"
                        "#pushButton_2 {\n"
                        "background-color: #F4DF96;\n"
                        "border-radius:15%;\n"
                        "border: 1px solid gray;\n"
                        "}" )



