from addnote import Ui_AddNote
from editnote import Ui_EditNoteDialog
from delnote import Ui_DelNote
from opennote import Ui_OpenNoteTwo
from mainwindowdaily import Ui_MainWindowDaily
from PyQt5 import QtWidgets
import sys
from datetime import datetime
import json
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QLCDNumber,
    QDialog,
    QMainWindow,
    QListWidgetItem
)
from PyQt5.QtCore import QDate, Qt, QTimer, QTime
from PyQt5.QtGui import QTextCharFormat, QColor
from os import path

from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QListWidgetItem, QSizePolicy

class AddNoteDialog(QDialog, Ui_AddNote):  # Наследуемся от QDialog и Ui_AddNote
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Добавление записи")

    def getInputs(self):
        mainNote = self.caption.text()
        additionalNote = self.description.toPlainText()
        print("Main note:", mainNote)
        print("Additional note:", additionalNote)
        return mainNote, additionalNote
    
    def reject(self):
        print("Cancel button clicked")
        super().reject()

class DailyPlanner(QMainWindow, Ui_MainWindowDaily):
    currentDay = str(datetime.now().day).rjust(2, "0")
    currentMonth = str(datetime.now().month).rjust(2, "0")
    currentYear = str(datetime.now().year).rjust(2, "0")

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Ежедневник")
        self.setFixedSize(861,465)
        self.initUI()

    def initUI(self):
        self.fmt = QTextCharFormat()
        self.fmt.setBackground(QColor(255, 165, 0, 100))
    
        self.data = {}
        file_exists = path.isfile(path.join(path.dirname(__file__), "data.json"))
        if file_exists:
            with open("data.json", "r") as json_file:
                self.data = json.load(json_file)

        self.cur_date = QDate.currentDate()

        for date in list(self.data.keys()):
            qdate = QDate.fromString(date, "ddMMyyyy")
            self.calendarWidget.setDateTextFormat(qdate, self.fmt)

        self.addButton = self.pushButton_3
        self.addButton.clicked.connect(self.addNote)

        self.editButton = self.pushButton_4
        self.editButton.clicked.connect(self.editNote)

        self.delButton = self.pushButton_5
        self.delButton.clicked.connect(self.delNote)

        self.calendarWidget.selectionChanged.connect(self.showDateInfo)
        self.calendarWidget.selectionChanged.connect(self.labelDate)
        self.calendarWidget.selectionChanged.connect(self.highlightFirstItem)
        self.calendarWidget.selectionChanged.connect(self.toggleAddEditDeleteButtons)
        self.calendarWidget.selectionChanged.connect(self.updateDateInfo)
 
        todayButton = self.pushButton_2
        todayButton.clicked.connect(self.selectToday)

        self.label = self.label_date
        self.labelDate()
        self.showDateInfo()
        self.listView.itemDoubleClicked.connect(self.showFullNote)

        self.lcd = self.lcdNumber
        self.lcd.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)
        self.lcd.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); color: white;")
        
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        self.showTime()

    def selectToday(self):
        self.calendarWidget.setSelectedDate(QDate.currentDate())

    def addNote(self):
        dialog = QtWidgets.QDialog()
        ui = Ui_AddNote()
        ui.setupUi(dialog)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            mainNote, additionalNote = ui.getInputs()
            if not mainNote:
                return
            # Получаем текущую выбранную дату
            date = self.getDate()

            self.calendarWidget.setDateTextFormat(QDate.fromString(date, "ddMMyyyy"), self.fmt)

            # Обновляем данные
            if date in self.data:
                self.data[date].append(f"{mainNote}: {additionalNote}" if additionalNote else mainNote)
            else:
                self.data[date] = [f"{mainNote}: {additionalNote}" if additionalNote else mainNote]

            # Сохраняем изменения в файл
            with open("data.json", "w") as json_file:
                json.dump(self.data, json_file)

            # Обновляем отображение заметок
            self.showDateInfo()

    def editNote(self):
            date = self.getDate()
            row = self.listView.currentRow()
            item = self.listView.item(row)

            if item:
                # Получаем полные данные из элемента списка
                note_data = item.data(Qt.UserRole)
                mainNote = note_data["mainNote"]
                additionalNote = note_data["additionalNote"]

                # Создаем диалоговое окно редактирования записей
                dialog = QtWidgets.QDialog()
                ui = Ui_EditNoteDialog()
                ui.setupUi(dialog)

                # Устанавливаем значения в поля диалогового окна через объект ui
                ui.caption.setPlainText(mainNote.strip())
                ui.description.setPlainText(additionalNote.strip())

                if dialog.exec_() == QDialog.Accepted:
                    editedMainNote, editedAdditionalNote = ui.getInputs()

                    # Убираем пробелы с обоих концов строк, полученных из диалогового окна
                    editedMainNote = editedMainNote.strip()
                    editedAdditionalNote = editedAdditionalNote.strip()
                    if not editedMainNote:
                        return
                    editedNote = f"{editedMainNote}: {editedAdditionalNote}" if editedAdditionalNote else editedMainNote

                    # Обновляем данные
                
                    self.data[date][row] = editedNote

                    # Обновляем отображение заметок
                    self.showDateInfo()

    def delNote(self):
        currentRow = self.listView.currentRow()
        if currentRow >= 0:
            item = self.listView.item(currentRow)
            if item:
                dialog = QDialog()
                ui = Ui_DelNote()
                ui.setupUi(dialog)
                if dialog.exec_() == QDialog.Accepted:
                    # Ваш код для удаления записи
                    print("Запись удалена")
                    # Получаем текущую выбранную дату
                    date = self.getDate()
                    print("Дата, для которой происходит удаление:", date)

                    # Удаляем запись и ее QListWidgetItem из списка записей
                    self.listView.takeItem(currentRow)

                    # Удаляем запись из данных
                    if date in self.data:
                        del self.data[date][currentRow]
                        if not self.data[date]:
                            del self.data[date]
                            self.calendarWidget.setDateTextFormat(QDate.fromString(date, "ddMMyyyy"), QTextCharFormat())
                            self.listView.clear()

                    # Сохраняем изменения в файл
                    with open("data.json", "w") as json_file:
                        json.dump(self.data, json_file)
                else:
                    print("Удаление отменено")
                    
    def showDateInfo(self):
        date = self.getDate()
        self.listView.clear()
        self.listView.setFixedWidth(401)
        if date in self.data:
            for note in self.data[date]:
                if isinstance(note, dict):  # Добавлено условие для проверки типа данных
                    mainNote = note["mainNote"]
                    additionalNote = note["additionalNote"]
                else:
                    # Проверяем, есть ли символ ":" в записи
                    if ":" in note:
                        mainNote, additionalNote = note.split(":", 1)
                    else:
                        # Если символ ":" отсутствует, считаем всю запись основной заметкой
                        mainNote = note
                        additionalNote = ""
                listItem, widget = createCustomListItem(str(mainNote), str(additionalNote))  # Преобразование в строки
                
                widget.setFixedWidth(300)

                self.listView.addItem(listItem)
                self.listView.setItemWidget(listItem, widget)

    def showTime(self):
        time = QTime.currentTime()
        text = time.toString("hh:mm")
        if time.second() % 2 == 0:
            text.replace(text[2], "")
        self.lcd.display(text)

    def getDate(self):
        select = self.calendarWidget.selectedDate()
        date = select.toString("ddMMyyyy")
        return date
    
    def closeEvent(self, e):
        with open("data.json", "w") as json_file:
            json.dump(self.data, json_file)
        e.accept()

    def labelDate(self):
        select = self.calendarWidget.selectedDate()
        weekday, month = select.dayOfWeek(), select.month()
        day, year = str(select.day()), str(select.year())
        week_day, word_month = QDate.longDayName(weekday), QDate.longMonthName(month)
        self.label_date.setText(week_day + ", " + word_month + " " + day + ", " + year)

    def toggleAddEditDeleteButtons(self):
        enabled = self.calendarWidget.selectedDate() >= QDate.currentDate()
        for button in [self.addButton, self.editButton, self.delButton]:
            button.setEnabled(enabled)
    
    def showFullNote(self, item):
        note_data = item.data(Qt.UserRole)
        mainNote = note_data["mainNote"]
        additionalNote = note_data["additionalNote"]
        dialog = QtWidgets.QDialog()
        ui = Ui_OpenNoteTwo()
        ui.setupUi(dialog, mainNote, additionalNote)
        # Извлекаем полные данные заметки

        dialog.exec_()

    def highlightFirstItem(self):
        if self.listView.count() > 0:
            self.listView.setCurrentRow(0)

    def updateDateInfo(self):
        self.showDateInfo()

def createCustomListItem(mainNote, additionalNote, max_length=50):
    # Создаем виджет, который будет содержать наш текст
    widget = QWidget()
    layout = QVBoxLayout(widget)

    # Создаем QLabel для mainNote, усекаем текст только для отображения
    mainNoteLabel = QLabel(mainNote)
    mainNoteLabel.setStyleSheet("font-family: Bahnschrift; font-size: 17px; font-weight: bold;")

    # Создаем QLabel для additionalNote, усекаем текст только для отображения
    truncatedAdditionalNote = truncate_text(additionalNote, max_length)
    additionalNoteLabel = QLabel(truncatedAdditionalNote)
    additionalNoteLabel.setMaximumWidth(280)  # Устанавливаем максимальную ширину для текста
    additionalNoteLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
    additionalNoteLabel.setStyleSheet("""
        font-family: Bahnschrift;
        font-size: 14px;
        color: black;
        white-space: nowrap;
        margin: 0;
        padding: 0;
    """)

    # Добавляем QLabel в layout
    layout.addWidget(mainNoteLabel)
    layout.addWidget(additionalNoteLabel)

    # Создаем QListWidgetItem и настраиваем размер виджета
    listItem = QListWidgetItem()
    listItem.setData(Qt.UserRole, {"mainNote": mainNote, "additionalNote": additionalNote})
    listItem.setSizeHint(widget.sizeHint())

    return listItem, widget

def truncate_text(text, max_length=50):
    lines = text.splitlines()
    if not lines:
        return ""

    first_line = lines[0].strip()

    # Если в тексте только одна строка и она короткая, не добавляем многоточие
    if len(lines) == 1 and len(first_line) <= max_length:
        return first_line

    # Если в первой строке больше одного слова и длина превышает max_length, обрезаем до max_length
    if len(first_line.split()) > 1 and len(first_line) > max_length:
        return first_line[:max_length-3] + "..."
    
    # Если в тексте более одной строки или одно длинное слово
    return first_line[:max_length] + "..." if len(first_line) > max_length or len(lines) > 1 else first_line

def main():
    app = QApplication(sys.argv)
    planner = DailyPlanner()
    planner.show()
    app.exec()

if __name__ == "__main__":
    main()
