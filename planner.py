from add_note_dialog import AddNoteDialog
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton, QDialogButtonBox, QInputDialog, QListWidgetItem
from PyQt5.QtCore import QDate
import sys
from datetime import datetime
import json
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QCalendarWidget,
    QLabel,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QInputDialog,
    QLCDNumber,
)
from PyQt5.QtCore import QDate, Qt, QTimer, QTime
from PyQt5 import QtGui
from PyQt5.QtGui import QTextCharFormat, QColor, QPixmap
from os import path

from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QListWidgetItem, QSizePolicy

def createCustomListItem(mainNote, additionalNote, max_length=50):
    # Создаем виджет, который будет содержать наш текст
    widget = QWidget()
    layout = QVBoxLayout(widget)

    # Создаем QLabel для mainNote, усекаем текст только для отображения
    mainNoteLabel = QLabel(mainNote)
    mainNoteLabel.setStyleSheet("font-weight: bold;")

    # Создаем QLabel для additionalNote, усекаем текст только для отображения
    truncatedAdditionalNote = truncate_text(additionalNote, max_length)
    additionalNoteLabel = QLabel(truncatedAdditionalNote)
    additionalNoteLabel.setMaximumWidth(280)  # Устанавливаем максимальную ширину для текста
    additionalNoteLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
    additionalNoteLabel.setStyleSheet("""
        font-size: 10px;
        color: black;
        text-overflow: ellipsis;
        overflow: hidden;
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

class Calendar(QWidget):
    currentDay = str(datetime.now().day).rjust(2, "0")
    currentMonth = str(datetime.now().month).rjust(2, "0")
    currentYear = str(datetime.now().year).rjust(2, "0")

    def __init__(self, width, height):
        super().__init__()
        folder = path.dirname(__file__)
        self.icon_folder = path.join(folder, "icons")

        self.setWindowTitle("Daily Planner")
        self.setWindowIcon(QtGui.QIcon(path.join(self.icon_folder, "window.png")))

        self.setGeometry(width // 4, height // 4, width // 2, height // 2)
        self.initUI()

   

    def initUI(self):
        self.first_run = True  # Добавляем переменную для отслеживания первого запуска программы
    
        self.first_run = False  # Устанавливаем значение False после инициализации пользовательского интерфейса
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)

        self.fmt = QTextCharFormat()
        self.fmt.setBackground(QColor(255, 165, 0, 100))

        cur_day_fmt = QTextCharFormat()
        cur_day_fmt.setBackground(QColor(0, 255, 90, 70))

        self.delfmt = QTextCharFormat()
        self.delfmt.setBackground(Qt.transparent)

        self.data = {}
        file_exists = path.isfile(path.join(path.dirname(__file__), "data.json"))
        if file_exists:
            with open("data.json", "r") as json_file:
                self.data = json.load(json_file)

        cur_date = QDate.currentDate()
        for date in list(self.data.keys()):
            qdate = QDate.fromString(date, "ddMMyyyy")
            self.calendar.setDateTextFormat(qdate, self.fmt)

        self.calendar.setDateTextFormat(cur_date, cur_day_fmt)

        self.addButton = QPushButton("Add Event")
        self.addButton.clicked.connect(self.addNote)
        self.editButton = QPushButton("Edit")
        self.editButton.clicked.connect(self.editNote)
        self.delButton = QPushButton("Delete")
        self.delButton.clicked.connect(self.delNote)

        self.calendar.selectionChanged.connect(self.showDateInfo)
        self.calendar.selectionChanged.connect(self.labelDate)
        self.calendar.selectionChanged.connect(self.highlightFirstItem)
        self.calendar.selectionChanged.connect(self.toggleAddEditDeleteButtons)
        self.calendar.selectionChanged.connect(self.updateDateInfo)

        self.note_group = QListWidget()
        self.note_group.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.note_group.setSortingEnabled(True)
        self.note_group.setStyleSheet("""
        QListView::item {
            height: 40px;
        }
        QListView {
            border-radius: 10px;
            border-width: 1px;
            border-color: rgba(0,0,0,80);
        }
    """)
        #self.note_group.setStyleSheet("QListView::item {width: 300px;}")
        todayButton = QPushButton("Today")
        todayButton.clicked.connect(self.selectToday)
        self.label = QLabel()
        label_font = QtGui.QFont("Arial", 16)
        self.label.setFont(label_font)
        self.labelDate()
        self.showDateInfo()
        self.note_group.itemDoubleClicked.connect(self.showFullNote)

        labelp = QLabel()
        pixmap = QPixmap(path.join(self.icon_folder, "calendar.png"))
        labelp.setPixmap(pixmap)

        self.lcd = QLCDNumber()
        self.lcd.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)
        self.lcd.setMinimumWidth(80)
        self.lcd.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); color: white;")
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        self.showTime()

        hbox1 = QHBoxLayout()
        hbox1.addWidget(todayButton)
        hbox1.addStretch(1)
        hbox1.addWidget(self.label)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.addButton)
        hbox2.addWidget(self.editButton)
        hbox2.addWidget(self.delButton)

        hbox3 = QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addWidget(labelp)
        hbox3.addWidget(self.lcd)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addWidget(self.note_group)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)

        hbox = QHBoxLayout()
        hbox.addWidget(self.calendar, 55)
        hbox.addLayout(vbox, 45)

        self.setLayout(hbox)

    def showDateInfo(self):
        try:
            date = self.getDate()
            self.note_group.clear()
            self.note_group.setFixedWidth(300)
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

                    self.note_group.addItem(listItem)
                    self.note_group.setItemWidget(listItem, widget)
            else:
                # Проверяем, если файл пустой или это первый запуск программы, то не выводим сообщение
                if not self.data or not self.first_run:
                    return
                QMessageBox.information(self, "No Notes", "There are no notes for the selected date.")
        except Exception as e:
            print("An error occurred in showDateInfo:", e)

    def updateDateInfo(self):
        self.showDateInfo()

    def selectToday(self):
        self.calendar.setSelectedDate(QDate.currentDate())

    def toggleAddEditDeleteButtons(self):
        enabled = self.calendar.selectedDate() >= QDate.currentDate()
        for button in [self.addButton, self.editButton, self.delButton]:
            button.setEnabled(enabled)
    
    def showFullNote(self, item):
        # Извлекаем полные данные заметки
        note_data = item.data(Qt.UserRole)
        mainNote = note_data["mainNote"]
        additionalNote = note_data["additionalNote"]
        QMessageBox.information(self, "Full Note", f"{mainNote}\n{additionalNote}")

    def addNote(self):
        try:
            dialog = AddNoteDialog(self)
            if dialog.exec_() == QDialog.Accepted:
                mainNote, additionalNote = dialog.getInputs()
                if not mainNote:
                    return
                # Получаем текущую выбранную дату
                date = self.getDate()

                self.calendar.setDateTextFormat(QDate.fromString(date, "ddMMyyyy"), self.fmt)

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

        except Exception as e:
            print("An error occurred:", e)

    def delNote(self):
        try:
            currentRow = self.note_group.currentRow()
            if currentRow >= 0:
                item = self.note_group.item(currentRow)
                if item:
                    reply = QMessageBox.question(
                        self, "Confirm Deletion", "Are you sure you want to delete this note?",
                        QMessageBox.Yes | QMessageBox.No
                    )
                    if reply == QMessageBox.Yes:
                        # Получаем текущую выбранную дату
                        date = self.getDate()

                        # Удаляем запись и ее QListWidgetItem из списка записей
                        self.note_group.takeItem(currentRow)

                        # Удаляем запись из данных
                        if date in self.data:
                            print("otladka", currentRow)
                            leng = len(self.data[date])
                            print("otladka", leng)
                            if leng > 1:
                                for_searh = leng-1 - currentRow
                            else:
                                for_searh = currentRow
                            del self.data[date][for_searh]
                            if not self.data[date]:
                                del self.data[date]
                                self.calendar.setDateTextFormat(QDate.fromString(date, "ddMMyyyy"), self.delfmt)

                        # Сохраняем изменения в файл
                        with open("data.json", "w") as json_file:
                            json.dump(self.data, json_file)
        except Exception as e:
            print("An error occurred:", e)
            
    def editNote(self):
        date = self.getDate()
        row = self.note_group.currentRow()
        item = self.note_group.item(row)

        if item:
            # Получаем полные данные из элемента списка
            note_data = item.data(Qt.UserRole)
            mainNote = note_data["mainNote"]
            additionalNote = note_data["additionalNote"]

            dialog = AddNoteDialog(self)
            dialog.firstInput.setText(mainNote.strip())  # Убираем пробелы
            dialog.secondInput.setText(additionalNote.strip())  # Убираем пробелы

            if dialog.exec_() == QDialog.Accepted:
                editedMainNote, editedAdditionalNote = dialog.getInputs()

                # Убираем пробелы с обоих концов строк, полученных из диалогового окна
                editedMainNote = editedMainNote.strip()
                editedAdditionalNote = editedAdditionalNote.strip()
                if not editedMainNote:
                    return
                editedNote = f"{editedMainNote}: {editedAdditionalNote}" if editedAdditionalNote else editedMainNote

                # Обновляем данные
                for_search = len(self.data[date]) - 1 - row if len(self.data[date]) > 1 else row
                self.data[date][for_search] = editedNote

                # Обновляем отображение заметок
                self.showDateInfo()


    def getDate(self):
        select = self.calendar.selectedDate()
        date = select.toString("ddMMyyyy")
        return date

    def labelDate(self):
        select = self.calendar.selectedDate()
        weekday, month = select.dayOfWeek(), select.month()
        day, year = str(select.day()), str(select.year())
        week_day, word_month = QDate.longDayName(weekday), QDate.longMonthName(month)
        self.label.setText(week_day + ", " + word_month + " " + day + ", " + year)

    def highlightFirstItem(self):
        if self.note_group.count() > 0:
            self.note_group.setCurrentRow(0)

    def showTime(self):
        time = QTime.currentTime()
        text = time.toString("hh:mm")
        if time.second() % 2 == 0:
            text.replace(text[2], "")
        self.lcd.display(text)

    def closeEvent(self, e):
        with open("data.json", "w") as json_file:
            json.dump(self.data, json_file)
        e.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QPushButton {border-style: solid; border-radius: 5px; \
                           border-width: 1px; border-color: rgba(0,0,0,80); padding: 5px} \
              QPushButton:hover {background-color: rgba(0, 0, 255, 0.05)} \
              QListWidget {background-color: rgb(230, 230, 230); border-style: solid;\
                           border-radius: 10px; border-width: 1px; border-color: rgba(0,0,0,80); width: 300px;} \
              QListWidget::item:selected {background-color: rgba(0, 0, 255, 0.1); border-radius: 10px; \
                                          border-style: solid; border-width: 1px; border-color: rgba(0,0,0,80); \
                                          color: black}\
              QListWidget::item:hover {background-color: rgba(0, 255, 0, 0.1); border-radius: 10px; \
                                       border-style: solid; border-width: 1px; border-color: rgba(0,0,0,80)}\
              QLCDNumber {border-style: solid; border-radius: 8px; background-color: rgb(230, 230, 230); \
                          border-width: 1px; border-color: rgba(0,0,0,80);")

    screen = app.primaryScreen()
    size = screen.size()
    window = Calendar(size.width(), size.height())
    window.show()
    sys.exit(app.exec_())
