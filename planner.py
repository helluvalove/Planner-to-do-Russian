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

def createCustomListItem(mainNote, additionalNote):
        # Создаем виджет, который будет содержать наш текст
        widget = QWidget()
        layout = QVBoxLayout()

        # Создаем два QLabel для mainNote и additionalNote
        mainNoteLabel = QLabel(mainNote)
        additionalNoteLabel = QLabel(additionalNote)
        mainNoteLabel.setStyleSheet("font-weight: bold;")
        additionalNoteLabel.setStyleSheet("font-size: 10px;")  # Скрываем текст, если он длинный

        # Добавляем QLabel в layout
        layout.addWidget(mainNoteLabel)
        layout.addWidget(additionalNoteLabel)
        widget.setLayout(layout)

        # Создаем QListWidgetItem
        listItem = QListWidgetItem()

        # Важно! Настраиваем размер виджета в соответствии с содержимым
        listItem.setSizeHint(widget.sizeHint())

        return listItem, widget 

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
        self.note_group.setSortingEnabled(True)
        self.note_group.setStyleSheet("QListView::item {height: 40px;}")

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
        self.lcd.setSegmentStyle(QLCDNumber.Filled)
        self.lcd.setMinimumWidth(80)
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
        widget = self.note_group.itemWidget(item)
        mainNote = widget.layout().itemAt(0).widget().text()
        additionalNote = widget.layout().itemAt(1).widget().text()
        QMessageBox.information(self, "Full Note", f"{mainNote}\n{additionalNote}")

    def addNote(self):
        try:
            dialog = AddNoteDialog(self)
            if dialog.exec_() == QDialog.Accepted:
                mainNote, additionalNote = dialog.getInputs()

                # Получаем текущую выбранную дату
                date = self.getDate()

                # Проверяем, не начинается ли основная заметка с цифры, отличной от 0, 1, 2
                if mainNote and mainNote[0].isdigit() and mainNote[0] not in ["0", "1", "2"]:
                    mainNote = "0" + mainNote

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
                            del self.data[date][currentRow]
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
            widget = self.note_group.itemWidget(item)
            mainNote = widget.layout().itemAt(0).widget().text()
            additionalNote = widget.layout().itemAt(1).widget().text()

            dialog = AddNoteDialog(self)
            dialog.firstInput.setText(mainNote)
            dialog.secondInput.setText(additionalNote)

            if dialog.exec_() == QDialog.Accepted:
                editedMainNote, editedAdditionalNote = dialog.getInputs()

                editedNote = f"{editedMainNote}: {editedAdditionalNote}" if editedAdditionalNote else editedMainNote
                self.data[date][row] = editedNote

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
                           border-radius: 10px; border-width: 1px; border-color: rgba(0,0,0,80);} \
              QListWidget::item:selected {background-color: rgba(0, 0, 255, 0.1); border-radius: 10px; \
                                          border-style: solid; border-width: 1px; border-color: rgba(0,0,0,80); \
                                          color: black}\
              QListWidget::item:hover {background-color: rgba(0, 255, 0, 0.1); border-radius: 10px; \
                                       border-style: solid; border-width: 1px; border-color: rgba(0,0,0,80)}\
              QLCDNumber {border-style: solid; border-radius: 8px; background-color: rgb(230, 230, 230); \
                          border-width: 1px; border-color: rgba(0,0,0,80);}")
    screen = app.primaryScreen()
    size = screen.size()
    window = Calendar(size.width(), size.height())
    window.show()
    sys.exit(app.exec_())