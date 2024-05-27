from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton

class HighlightButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMouseTracking(True)

    def enterEvent(self, event):
        self.setStyleSheet("#pushButton_2:hover, #pushButton_3:hover, #pushButton_4:hover, #pushButton_5:hover, #pushButton_6:hover {\n"
                            "background-color: #dbb44b;\n"
                            "}")

class Ui_MainWindowDaily(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 500)
        font = QtGui.QFont("Bahnschrift Light", 14)
        button_font = QtGui.QFont("Bahnschrift Light", 13)
        label_font = QtGui.QFont("Bahnschrift", 18)
        MainWindow.setFont(font)
        self.centralWidget = QtWidgets.QWidget(MainWindow)  
        self.centralWidget.setStyleSheet("#centralwidget {\n"
"background-color: #FCF1C9;\n"
"}")
        self.centralWidget.setObjectName("centralwidget")
        self.centralWidget.setFont(font)  
        self.pushButton_2 = HighlightButton(self.centralWidget)  
        self.pushButton_2.setFont(button_font)  
        self.pushButton_2.setGeometry(QtCore.QRect(440, 20, 111, 41))
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_2.setMouseTracking(False)
        self.pushButton_2.setStyleSheet("#pushButton_2 {\n"
                                "background-color: #F4DF96;\n"
                                "border-radius:15%;\n"
                                "border: 1px solid gray;\n"
                                "}")
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_6 = HighlightButton(self.centralWidget)
        self.pushButton_6.setFont(button_font)
        self.pushButton_6.setGeometry(QtCore.QRect(440, 430, 300, 35))
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_6.setMouseTracking(False)
        self.pushButton_6.setStyleSheet("#pushButton_6 {\n"
                                        "background-color: #F4DF96;\n"
                                        "border-radius:15%;\n"
                                        "border: 1px solid gray;\n"
                                        "}")
        self.pushButton_6.setObjectName("pushButton_6")

        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralWidget) 
        self.calendarWidget.setGeometry(QtCore.QRect(20, 20, 401, 401))
        self.calendarWidget.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.calendarWidget.setToolTip("")
        self.calendarWidget.setStatusTip("")
        self.calendarWidget.setAutoFillBackground(True)
        self.calendarWidget.setStyleSheet("#calendarWidget QWidget {\n"
"    alternate-background-color: #F4DF96;\n"
"}\n"
"\n"
"#qt_calendar_navigationbar {\n"
"    background-color: #fff;\n"
"    border: 2px solid #F4DF96;\n"
"    border-bottom: 0px;\n"
"    border-top-left-radius: 5px;\n"
"    border-top-right-radius: 5px;\n"
"}\n"
"\n"
"#qt_calendar_prevmonth,\n"
"#qt_calendar_nextmonth {\n"
"    border: none;\n"
"\n"
"    min-width: 13px;\n"
"    max-width: 13px;\n"
"    min-height: 13px;\n"
"    max-height: 13px;\n"
"\n"
"    border-radius: 5px;\n"
"    background-color: transparent;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"#qt_calendar_prevmonth {\n"
"    margin-left: 5px;\n"
"}\n"
"\n"
"#qt_calendar_nextmonth {\n"
"    margin-right: 5px;\n"
"}\n"
"\n"
"#qt_calendar_prevmonth:hover,\n"
"#qt_calendar_nextmonth:hover {\n"
"    background-color: #F4DF96;\n"
"}\n"
"\n"
"#qt_calendar_prevmonth:pressed,\n"
"#qt_calendar_nextmonth:pressed {\n"
"    background-color: #F4DF96;\n"
"}\n"
"\n"
"#qt_calendar_yearbutton {\n"
"    color:#000;\n"
"    margin: 5px;\n"
"    border-radius: 5px;\n"
"    font-size: 13px;\n"
"    padding: 0 10px;\n"
"}\n"
"\n"
"#qt_calendar_monthbutton {\n"
"    width: 110px;\n"
"    color: #000;\n"
"    font-size: 13px;\n"
"    margin: 5px 0;\n"
"    border-radius: 5px;\n"
"    padding: 0px 2px;\n"
"}\n"
"\n"
"#qt_calendar_yearbutton:hover,\n"
"#qt_calendar_monthbutton:hover {\n"
"    background-color: #F4DF96;\n"
"}\n"
"\n"
"#qt_calendar_yearbutton:pressed,\n"
"#qt_calendar_monthbutton:pressed {\n"
"    background-color: #F4DF96;\n"
"}\n"
"\n"
"#qt_calendar_yearedit {\n"
"    min-width: 53px;\n"
"    color: #000;\n"
"    background: transparent;\n"
"    font-size: 13px;\n"
"}\n"
"\n"
"\n"
"#calendarWidget QToolButton QMenu {\n"
"    background-color: #F4DF96;\n"
"}\n"
"\n"
"#calendarWidget QToolButton QMenu::item {\n"
"    /* padding: 5px; */\n"
"}\n"
"\n"
"#calendarWidget QToolButton QMenu::itemselected:enabled {\n"
"     background-color: #F4DF96;\n"
"}\n"
"\n"
"#calendarWidget QToolButton::menu-indicator {\n"
"    subcontrol-position: right center;\n"
"    margin-top: 10px;\n"
"    width: 20px;\n"
"}\n"
"\n"
"#qt_calendar_calendarview {\n"
"    border: 2px solid #F4DF96;\n"
"    border-top: 0px;\n"
"    border-bottom-left-radius: 5px;\n"
"    border-bottom-right-radius: 5px;\n"
"}\n"
"\n"
"#qt_calendar_calendarview::item:hover {\n"
"    border-radius: 5px;\n"
"    background-color: #aaffff;\n"
"}\n"
"\n"
"#qt_calendar_calendarview::item:selected {\n"
"    border-radius: 5px;\n"
"    background-color: #F4DF96;\n"
"}")
        self.calendarWidget.setGridVisible(False)
        self.calendarWidget.setObjectName("calendarWidget")
        self.pushButton_3 = HighlightButton(self.centralWidget)  
        self.pushButton_3.setFont(button_font) 
        self.pushButton_3.setGeometry(QtCore.QRect(440, 380, 121, 41))
        self.pushButton_3.setStyleSheet("#pushButton_3 {\n"
"background-color: #F4DF96;\n"
"border-radius:15%;\n"
"border: 1px solid gray;\n"
"}")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = HighlightButton(self.centralWidget)  
        self.pushButton_4.setFont(button_font)  
        self.pushButton_4.setGeometry(QtCore.QRect(580, 380, 121, 41))
        self.pushButton_4.setStyleSheet("#pushButton_4 {\n"
"background-color: #F4DF96;\n"
"border-radius:15%;\n"
"border: 1px solid gray;\n"
"}")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = HighlightButton(self.centralWidget)  
        self.pushButton_5.setFont(button_font) 
        self.pushButton_5.setGeometry(QtCore.QRect(720, 380, 121, 41))
        self.pushButton_5.setStyleSheet("#pushButton_5 {\n"
"background-color: #F4DF96;\n"
"border-radius:15%;\n"
"border: 1px solid gray;\n"
"}")
        self.pushButton_5.setObjectName("pushButton_5")
        self.label_date = QtWidgets.QLabel(self.centralWidget) 
        self.label_date.setFont(label_font)
        self.label_date.setGeometry(QtCore.QRect(580, 20, 251, 41))
        self.label_date.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_date.setObjectName("label")
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralWidget)  
        self.lcdNumber.setFont(font)  
        self.lcdNumber.setGeometry(QtCore.QRect(770, 430, 64, 23))
        self.lcdNumber.setMinimumWidth(80) 
        self.lcdNumber.setObjectName("lcdNumber")
        self.scrollArea = QtWidgets.QScrollArea(self.centralWidget)  
        self.scrollArea.setFont(font)
        self.scrollArea.setGeometry(QtCore.QRect(440, 70, 401, 291))
        self.scrollArea.setStyleSheet("#scrollArea {\n"
"border-radius: 70%;\n"
"}")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollAreaWidgetContents = QtWidgets.QWidget(self.scrollArea)
        self.scrollAreaWidgetContents.setFont(font)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 401, 291))
        self.scrollAreaWidgetContents.setStyleSheet("#scrollAreaWidgetContents {\n"
"border-radius: 50%;\n"
"}")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.listView = QtWidgets.QListWidget(self.scrollAreaWidgetContents)
        self.listView.setFont(font)  
        self.listView.setGeometry(QtCore.QRect(0, 0, 401, 291))
        self.listView.setStyleSheet("""
        QListView::item {
            height: 40px;
        }
        QListView {
            border: 1px solid gray;
            border-width: 1px;
            border-color: rgba(0,0,0,80);
        }
    """)
        self.listView.setObjectName("listView")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Ежедневник"))
        self.pushButton_2.setText(_translate("MainWindow", "Сегодня"))
        self.pushButton_3.setText(_translate("MainWindow", "Добавить"))
        self.pushButton_4.setText(_translate("MainWindow", "Изменить"))
        self.pushButton_5.setText(_translate("MainWindow", "Удалить"))
        self.pushButton_6.setText(_translate("MainWindow", "Изменить пароль"))
        self.label_date.setText(_translate("MainWindow", "Суббота, Апрель 20, 2024"))


    def enterEvent(self, event):
        self.setStyleSheet("#pushButton_2:hover, #pushButton_3:hover, #pushButton_4:hover, #pushButton_5:hover, #pushButton_6:hover {\n"
                        "background-color: #F8E71C;\n"
                        "}"
                           
                        "#pushButton_2 {\n"
                        "background-color: #F4DF96;\n"
                        "border-radius:15%;\n"
                        "border: 1px solid gray;\n"
                        "}"
                           
                        "#pushButton_3 {\n"
                        "background-color: #F4DF96;\n"
                        "border-radius:15%;\n"
                        "border: 1px solid gray;\n"
                        "}" 
                           
                        "#pushButton_4 {\n"
                        "background-color: #F4DF96;\n"
                        "border-radius:15%;\n"
                        "border: 1px solid gray;\n"
                        "}"
                           
                        "#pushButton_5 {\n"
                        "background-color: #F4DF96;\n"
                        "border-radius:15%;\n"
                        "border: 1px solid gray;\n"
                        "}"
                           
                        "#pushButton_6 {\n"
                        "background-color: #F4DF96;\n"
                        "border-radius:15%;\n"
                        "border: 1px solid gray;\n"   
                        "}"
)



