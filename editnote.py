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
        
class Ui_EditNoteDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(351, 402)
        Dialog.setStyleSheet("#Dialog {\n"
"background-color: #FCF1C9;\n"
"}")
        font = QtGui.QFont("Bahnschrift Light", 15)
        button_font = QtGui.QFont("Bahnschrift Light", 13)
        text_font = QtGui.QFont("Bahnschrift Light", 13)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 101, 16))
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setFont(font)
        self.scrollArea.setGeometry(QtCore.QRect(20, 50, 311, 31))
        self.scrollArea.setStyleSheet("#scrollArea{\n"
"background-color: #FCF1C9;\n"
"}")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setFont(font)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 309, 29))
        self.scrollAreaWidgetContents.setStyleSheet("#scrollAreaWidgetContents {\n"
"background-color: transparent;\n"
"}")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.caption = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
        self.caption.setFont(text_font)
        self.caption.setObjectName("caption")
        self.caption.setGeometry(QtCore.QRect(0, 0, 311, 100))
        self.caption.textChanged.connect(self.limitCaptionLength)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 90, 161, 21))
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.scrollArea_2 = QtWidgets.QScrollArea(Dialog)
        self.scrollArea_2.setFont(font)
        self.scrollArea_2.setGeometry(QtCore.QRect(20, 120, 311, 231))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setFont(font)
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 309, 229))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.description = QtWidgets.QPlainTextEdit(self.scrollAreaWidgetContents_2)
        self.description.setFont(text_font)
        self.description.setObjectName("description")
        self.description.setGeometry(QtCore.QRect(0, 0, 311, 231))
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.pushButton = HighlightButton(Dialog)
        self.pushButton.setFont(button_font)
        self.pushButton.setGeometry(QtCore.QRect(190, 360, 81, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(Dialog.reject)
        self.pushButton_2 = HighlightButton(Dialog)
        self.pushButton_2.setFont(button_font)
        self.pushButton_2.setGeometry(QtCore.QRect(280, 360, 51, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(Dialog.accept)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def limitCaptionLength(self):
        max_length = 40
        if len(self.caption.toPlainText()) > max_length:
            cursor = self.caption.textCursor()
            cursor.deletePreviousChar()    

    def getInputs(self):
        return self.caption.toPlainText(), self.description.toPlainText()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Изменение заметки"))
        Dialog.setFixedSize(351,402)
        self.label.setText(_translate("Dialog", "Заголовок:"))
        self.label_2.setText(_translate("Dialog", "Запись:"))
        self.pushButton.setText(_translate("Dialog", "Отмена"))
        self.pushButton_2.setText(_translate("Dialog", "Ок"))

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