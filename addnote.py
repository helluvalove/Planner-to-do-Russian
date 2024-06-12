import platform
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QPushButton
from screeninfo import get_monitors
try:
    from Quartz import CGDisplayBounds, CGMainDisplayID, CGDisplayScreenSize
    print("Quartz imported successfully.")
except ImportError as e:
    print(f"Error importing Quartz: {e}")
from cryptography.fernet import Fernet, InvalidToken

def get_screen_density_windows():
    monitors = get_monitors()
    for monitor in monitors:
        width_mm = monitor.width_mm  # Ширина экрана в миллиметрах
        height_mm = monitor.height_mm  # Высота экрана в миллиметрах
        width_px = monitor.width  # Ширина экрана в пикселях
        height_px = monitor.height  # Высота экрана в пикселях

        # Плотность пикселей (PPI - pixels per inch)
        width_dpi = (width_px / (width_mm / 25.4))
        height_dpi = (height_px / (height_mm / 25.4))

        return width_dpi, height_dpi

def get_screen_density_mac():
    display_id = CGMainDisplayID()
    display_bounds = CGDisplayBounds(display_id)
    display_width_px = display_bounds.size.width
    display_height_px = display_bounds.size.height
    display_size_mm = CGDisplayScreenSize(display_id)
    display_width_mm = display_size_mm.width
    display_height_mm = display_size_mm.height

    # Плотность пикселей (PPI - pixels per inch)
    width_dpi = (display_width_px / (display_width_mm / 25.4))
    height_dpi = (display_height_px / (display_height_mm / 25.4))

    return width_dpi, height_dpi

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

class EnterKeyFilter(QtCore.QObject):
    def __init__(self, max_width, parent=None):
        super().__init__(parent)
        self.max_width = max_width

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Return:
                # Prevent the Enter key event from being propagated
                return True
            elif (obj.isWidgetType() and isinstance(obj, QtWidgets.QTextEdit)) and event.key() != QtCore.Qt.Key_Backspace and event.key() != QtCore.Qt.Key_Delete:
                # Measure the width of the text
                font_metrics = obj.fontMetrics()
                text_width = font_metrics.horizontalAdvance(obj.toPlainText() + event.text())
                if text_width > self.max_width:
                    return True
        return super().eventFilter(obj, event)

class Ui_AddNote(object):

    def __init__(self):
        self.enterKeyFilter = None
        if platform.system() == 'Darwin':
            from Quartz import CGDisplayBounds, CGMainDisplayID, CGDisplayScreenSize
            width_dpi, height_dpi = get_screen_density_mac()
            self.average_dpi = (width_dpi + height_dpi) / 2
        else:
            width_dpi, height_dpi = get_screen_density_windows()
            self.average_dpi = (width_dpi + height_dpi) / 2

    def setupUi(self, Dialog):
        Dialog.setWindowFlags(Dialog.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        Dialog.setObjectName("Dialog")
        new_width = int(351 * (self.average_dpi / 127.5))
        new_height = int(402 * (self.average_dpi / 127.5))
        Dialog.resize(new_width, new_height)
        Dialog.setStyleSheet("#Dialog {\n"
"background-color: #FCF1C9;\n"
"}")
        font = QtGui.QFont("Verdana")
        button_font = QtGui.QFont("Verdana")
        text_font = QtGui.QFont("Verdana")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(int(20 * (self.average_dpi / 127.5)), int(20 * (self.average_dpi / 127.5)), int(101 * (self.average_dpi / 127.5)), int(16 * (self.average_dpi / 127.5))))
        self.label.setFont(font)
        self.label.setStyleSheet(f"font-size: {int(16 * (self.average_dpi / 127.5))}px;")
        self.label.setObjectName("label")
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setFont(text_font)
        self.scrollArea.setGeometry(QtCore.QRect(int(20 * (self.average_dpi / 127.5)), int(50 * (self.average_dpi / 127.5)), int(311 * (self.average_dpi / 127.5)), int(31 * (self.average_dpi / 127.5))))
        self.scrollArea.setStyleSheet("#scrollArea{\n"
"background-color: #FCF1C9;\n"
"}")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setFont(text_font)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, int(309 * (self.average_dpi / 127.5)), int(29 * (self.average_dpi / 127.5))))
        self.scrollAreaWidgetContents.setStyleSheet("#scrollAreaWidgetContents {\n"
"background-color: transparent;\n"
"}")
        self.scrollAreaWidgetContents.setStyleSheet(f"font-size: {int(13 * (self.average_dpi / 127.5))}px;")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.installEventFilter(self.enterKeyFilter)
        self.caption = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
        self.caption.setObjectName("caption")
        self.caption.setGeometry(QtCore.QRect(0, 0, int(311 * (self.average_dpi / 127.5)), int(100 * (self.average_dpi / 127.5))))
        self.caption.setFont(text_font)
        self.label.setStyleSheet(f"font-size: {int(16 * (self.average_dpi / 127.5))}px;")

        self.max_width = self.scrollArea.width() - int(10 * (self.average_dpi / 127.5))  # Adjust based on desired padding
        self.enterKeyFilter = EnterKeyFilter(self.max_width)
        self.caption.installEventFilter(self.enterKeyFilter)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(int(20 * (self.average_dpi / 127.5)), int(90 * (self.average_dpi / 127.5)), int(161 * (self.average_dpi / 127.5)), int(21 * (self.average_dpi / 127.5))))
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(f"font-size: {int(16 * (self.average_dpi / 127.5))}px;")
        self.label_2.setObjectName("label_2")
        self.scrollArea_2 = QtWidgets.QScrollArea(Dialog)
        self.scrollArea_2.setFont(text_font)
        self.scrollArea_2.setStyleSheet(f"font-size: {int(13 * (self.average_dpi / 127.5))}px;")
        self.scrollArea_2.setGeometry(QtCore.QRect(int(20 * (self.average_dpi / 127.5)), int(120 * (self.average_dpi / 127.5)), int(311 * (self.average_dpi / 127.5)), int(231 * (self.average_dpi / 127.5))))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, int(309 * (self.average_dpi / 127.5)), int(229 * (self.average_dpi / 127.5))))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setFont(text_font)
        self.scrollAreaWidgetContents_2.setStyleSheet(f"font-size: {int(13 * (self.average_dpi / 127.5))}px;")
        self.description = QtWidgets.QPlainTextEdit(self.scrollAreaWidgetContents_2)
        self.description.setFont(text_font)
        self.description.setStyleSheet(f"font-size: {int(13 * (self.average_dpi / 127.5))}px;")
        self.description.setObjectName("description")
        self.description.setGeometry(QtCore.QRect(0, 0, int(311 * (self.average_dpi / 127.5)), int(231 * (self.average_dpi / 127.5))))
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.scrollArea_2.setFont(font)
        self.scrollArea_2.setStyleSheet(f"font-size: {int(16 * (self.average_dpi / 127.5))}px;")
        self.pushButton = HighlightButton(Dialog)
        self.pushButton.setFont(button_font)
        self.pushButton.setGeometry(QtCore.QRect(int(190 * (self.average_dpi / 127.5)), int(360 * (self.average_dpi / 127.5)), int(81 * (self.average_dpi / 127.5)), int(32 * (self.average_dpi / 127.5))))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(Dialog.reject)
        self.pushButton_2 = HighlightButton(Dialog)
        self.pushButton_2.setFont(button_font)
        self.pushButton_2.setGeometry(QtCore.QRect(int(280 * (self.average_dpi / 127.5)), int(360 * (self.average_dpi / 127.5)), int(51 * (self.average_dpi / 127.5)), int(32 * (self.average_dpi / 127.5))))
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
        Dialog.setWindowTitle(_translate("Dialog", "Добавление заметки"))

        Dialog.setFixedSize(int(351 * (self.average_dpi / 127.5)), int(402 * (self.average_dpi / 127.5)))
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


