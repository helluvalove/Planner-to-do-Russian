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
        date = self.getDate()
        self.note_group.clear()
        if date in self.data:
            self.note_group.addItems(self.data[date])

    def selectToday(self):
        self.calendar.setSelectedDate(QDate.currentDate())

    def toggleAddEditDeleteButtons(self):
        enabled = self.calendar.selectedDate() >= QDate.currentDate()
        for button in [self.addButton, self.editButton, self.delButton]:
            button.setEnabled(enabled)

    def addNote(self):
        # adding notes for selected date
        # if a note starts with any number other than 0, 1, 2
        # add a 0 before it so that we can easily sort events
        # by start time
        date = self.getDate()
        row = self.note_group.currentRow()
        title = "Add event"
        string, ok = QInputDialog.getText(self, " ", title)

        if ok and string:
            if string[0].isdigit() and string[0] not in ["0", "1", "2"]:
                string = string.replace(string[0], "0" + string[0])
            self.note_group.insertItem(row, string)
            self.calendar.setDateTextFormat(
                QDate.fromString(date, "ddMMyyyy"), self.fmt
            )
            if date in self.data:
                self.data[date].append(string)
            else:
                self.data[date] = [string]

    def delNote(self):
        date = self.getDate()
        row = self.note_group.currentRow()
        item = self.note_group.item(row)

        if not item:
            return
        reply = QMessageBox.question(
            self, " ", "Remove", QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            item = self.note_group.takeItem(row)
            self.data[date].remove(item.text())
            if not self.data[date]:
                del self.data[date]
                self.calendar.setDateTextFormat(
                    QDate.fromString(date, "ddMMyyyy"), self.delfmt
                )
            del item

    def editNote(self):
        date = self.getDate()
        row = self.note_group.currentRow()
        item = self.note_group.item(row)

        if item:
            copy = item.text()
            title = "Edit event"
            string, ok = QInputDialog.getText(
                self, " ", title, QLineEdit.Normal, item.text()
            )

            if ok and string:
                self.data[date].remove(copy)
                self.data[date].append(string)
                if string[0].isdigit() and string[0] not in ["0", "1", "2"]:
                    string = string.replace(string[0], "0" + string[0])
                item.setText(string)

    def getDate(self):
        select = self.calendar.selectedDate()
        date = (
            str(select.day()).rjust(2, "0")
            + str(select.month()).rjust(2, "0")
            + str(select.year())
        )
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