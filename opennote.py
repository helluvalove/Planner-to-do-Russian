from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton, QTextBrowser

class HighlightButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMouseTracking(True)
        
        # Устанавливаем стили для обычного состояния кнопки
        self.setStyleSheet("QPushButton {\n"
                            "background-color: #F4DF96;\n"
                            "border-radius: 10%;\n"
                            "border: 1px solid gray;\n"
                            "}\n"
                            "QPushButton:hover {\n"
                            "background-color: #dbb44b;\n"
                            "}")

class Ui_OpenNoteTwo(object):
    def setupUi(self, MainWindow, MainNote, AdditionalNote):
        self.Main_note = MainNote
        self.Addit_note = AdditionalNote
        font = QtGui.QFont("Bahnschrift", 15)
        font_label = QtGui.QFont("Bahnschrift", 16)
        font_label.setBold(True)
        button_font = QtGui.QFont("Bahnschrift", 13)
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(438, 320)
        MainWindow.setStyleSheet("#MainWindow {\n"
"background-color: #FCF1C9;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setFont(font)
        self.centralwidget.setStyleSheet("#centralwidget {\n"
"background-color: #FCF1C9;\n"
"}")
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = HighlightButton(MainWindow)
        self.pushButton.setFont(button_font)
        self.pushButton.setGeometry(QtCore.QRect(360, 280, 61, 30))     
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(25, 30, 401, 21))
        self.label.setObjectName("label")
        self.label.setFont(font_label)

        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setFont(font)
        self.scrollArea.setGeometry(QtCore.QRect(20, 70, 401, 201))
        self.scrollArea.setStyleSheet("#scrollArea{\n"
"border: None;\n"
"background-color: #E32636;\n"
"}")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setFont(font)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 401, 201))
        self.scrollAreaWidgetContents.setStyleSheet("#scrollAreaWidgetContents{\n"
"border: None;\n"
"background-color: transparent;\n"
"}")
        self.scrollAreaWidgetContents.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        
        self.textBrowser = QTextBrowser(self.scrollAreaWidgetContents)  # Заменили на QTextBrowser
        self.textBrowser.setFont(font)
        self.textBrowser.setGeometry(QtCore.QRect(0, 0, 401, 201))
        self.textBrowser.setStyleSheet("#textBrowser{\n"
"border: None;\n"
"background-color: #FFFFFF;\n"
"border: 1px solid gray;\n"
"}")
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setOpenExternalLinks(False)  # Отключаем возможность открывать внешние ссылки
        self.textBrowser.setReadOnly(True)  
        self.textBrowser.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.pushButton.clicked.connect(MainWindow.accept)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Просмотр заметки"))
        MainWindow.setFixedSize(438, 320)
        self.pushButton.setText(_translate("MainWindow", "ОК"))
        self.label.setText(_translate("MainWindow", self.Main_note))
        
        # Check if there is additional note
        if not self.Addit_note:
            self.scrollArea.hide()
            self.textBrowser.hide()
            self.pushButton.setGeometry(QtCore.QRect(320, 80, 61, 30))
            MainWindow.setFixedSize(400, 120)
        else:
            self.textBrowser.setPlainText(self.Addit_note)
            self.pushButton.setGeometry(QtCore.QRect(360, 280, 61, 30))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_OpenNoteTwo()
    ui.setupUi(MainWindow, "Main Note", "Additional Note")
    MainWindow.show()
    sys.exit(app.exec_())