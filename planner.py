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
    QListWidgetItem, QSizePolicy, QMenu
)
from PyQt5.QtCore import QDate, Qt, QTimer, QTime, QLocale
from PyQt5.QtGui import QTextCharFormat, QColor
from PyQt5 import QtGui, QtWidgets
from os import path
from cryptography.fernet import Fernet, InvalidToken

# Замените на ваш сгенерированный ключ
ENCRYPTION_KEY = b'aSO-mTaOE72BQS3Nm1hvX_yO5yDEHTYUI207oFYI8Cs='
fernet = Fernet(ENCRYPTION_KEY)
DATA_FILE = "data.json"  # Define the path to the data file

class PasswordDialog(QDialog):
    def __init__(self, is_first_time, parent=None):
        super().__init__(parent)
        self.setObjectName('enter_pass')
        self.is_first_time = is_first_time
        self.setWindowTitle('Установите пароль' if is_first_time else 'Вход')
        self.setFixedSize(300, 150)
        font = QtGui.QFont("Bahnschrift", 14)
        self.setFont(font)
        self.setStyleSheet("#enter_pass {\n"
                           "background-color: #FCF1C9"
                           "}"
                           "QPushButton {\n"
                            "background-color: #F4DF96;\n"
                            "border-radius: 9%;\n"
                            "border: 1px solid gray;\n"
                            "width: 55px;"
                            "height: 25px;"
                            "}\n"
                            "QPushButton:hover {\n"
                            "background-color: #dbb44b;\n"
                            "}")

        self.layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel('Установите пароль:' if is_first_time else 'Введите свой пароль:')
        self.label.setStyleSheet("font-weight: bold;")
        self.layout.addWidget(self.label)

        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.button(QtWidgets.QDialogButtonBox.Ok).setText('Ок')
        self.button_box.button(QtWidgets.QDialogButtonBox.Cancel).setText('Отмена')
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)

    def accept(self):
        password = self.get_password()
        if 4 <= len(password) <= 12:
            super().accept()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setStyleSheet("QMessageBox {background-color: #FCF1C9}\n"
                              "QPushButton {\n"
                              "background-color: #F4DF96;\n"
                              "border-radius: 9%;\n"
                              "border: 1px solid gray;\n"
                              "width: 55px;\n"
                              "height: 25px;\n"
                              "}\n"
                              "QPushButton:hover {\n"
                              "background-color: #dbb44b;\n"
                              "}")
            msg.setText('Пароль должен содержать от 4 до 12 символов')
            msg.setWindowTitle('Ошибка')
            msg.exec_()

    def get_password(self):
        return self.password_input.text()

PASSWORD_FILE = "password_data.json"  # Define the path to the password file

def save_password(password):
    # Save only non-empty passwords
    if password:
        encrypted_password = fernet.encrypt(password.encode()).decode()
        data = {'password': encrypted_password}
    else:
        data = {}

    with open(PASSWORD_FILE, 'w') as file:
        json.dump(data, file)

def load_password():
    if not path.exists(PASSWORD_FILE):
        return None
    with open(PASSWORD_FILE, 'r') as file:
        data = json.load(file)
    encrypted_password = data.get('password')
    if encrypted_password:
        try:
            return fernet.decrypt(encrypted_password.encode()).decode()
        except InvalidToken as e:
            print(f"Error decrypting password: {e}")
            return None
    return None

class AddNoteDialog(QDialog, Ui_AddNote):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Добавление записи")

    def getInputs(self):
        mainNote = self.caption.text()
        additionalNote = self.description.toPlainText()
        return mainNote, additionalNote

    def reject(self):
        super().reject()

class DailyPlanner(QMainWindow, Ui_MainWindowDaily):
    currentDay = str(datetime.now().day).rjust(2, "0")
    currentMonth = str(datetime.now().month).rjust(2, "0")
    currentYear = str(datetime.now().year).rjust(2, "0")

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Ежедневник")
        self.setFixedSize(861, 490)
        self.initUI()

    def initUI(self):
        self.fmt = QTextCharFormat()
        self.fmt.setBackground(QColor(255, 165, 0, 100))

        self.data = {}
        if path.isfile(DATA_FILE):
            with open(DATA_FILE, "r") as json_file:
                encrypted_data = json.load(json_file)
                try:
                    self.data = {date: [self.decrypt_data(note) for note in notes] for date, notes in encrypted_data.items()}
                except InvalidToken as e:
                    print(f"Error decrypting data: {e}")
                    self.data = {}

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

        self.pushButton_6.clicked.connect(change_pass)

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
        self.listView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listView.customContextMenuRequested.connect(self.contextMenuEvent)

        self.lcd = self.lcdNumber
        self.lcd.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)
        self.lcd.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); color: white;")

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        self.showTime()

    def contextMenuEvent(self, position):
        try:
            menu = QMenu()
            addPointerAction = menu.addAction("Закрепить/открепить заметку")
            action = menu.exec_(self.listView.viewport().mapToGlobal(position))

            if action == addPointerAction:
                self.togglePointerInNote()

        except Exception as e:
            print(f"Error handling context menu event: {e}")

    def togglePointerInNote(self):
        currentRow = self.listView.currentRow()
        if currentRow >= 0:
            date = self.getDate()
            note_data = self.data[date][currentRow]
            decrypted_note = self.decrypt_data(note_data)

            if decrypted_note.startswith("📌"):
                decrypted_note = decrypted_note[2:].strip()  # Удаляем символ и пробел после него
            else:
                decrypted_note = "📌 " + decrypted_note

            encrypted_note = self.encrypt_data(decrypted_note)
            self.data[date][currentRow] = encrypted_note
            self.saveData()
            self.showDateInfo()

    def selectToday(self):
        self.calendarWidget.setSelectedDate(QDate.currentDate())

    def encrypt_data(self, data):
        return fernet.encrypt(data.encode()).decode()

    def decrypt_data(self, encrypted_data):
        try:
            return fernet.decrypt(encrypted_data.encode()).decode()
        except InvalidToken as e:
            print(f"Error decrypting data: {e}")
            return ""

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
            note = f"{mainNote}: {additionalNote}" if additionalNote else mainNote
            encrypted_note = self.encrypt_data(note)
            if date in self.data:
                self.data[date].append(encrypted_note)
            else:
                self.data[date] = [encrypted_note]

            # Сохраняем изменения в файл
            self.saveData()

            # Обновляем отображение заметок
            self.showDateInfo()

    def editNote(self):
        date = self.getDate()
        row = self.listView.currentRow()
        item = self.listView.item(row)

        if item:
            # Получаем полные данные из элемента списка
            note_data = self.decrypt_data(self.data[date][row])
            mainNote, additionalNote = (note_data.split(":", 1) + [""])[:2]  # Разделяем данные на основную и дополнительную часть

            # Убираем "📌" из заголовка, если он там есть
            if mainNote.startswith("📌"):
                mainNote = mainNote[2:].strip()

            # Создаем диалоговое окно редактирования записей
            dialog = QDialog()
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
                if note_data.startswith("📌"):  # Проверяем, была ли заметка закреплена
                    editedMainNote = "📌 " + editedMainNote  # Возвращаем "📌" в заголовок, если заметка была закреплена
                editedNote = f"{editedMainNote}: {editedAdditionalNote}" if editedAdditionalNote else editedMainNote
                encrypted_note = self.encrypt_data(editedNote)

                # Обновляем данные
                self.data[date][row] = encrypted_note

                # Сохраняем изменения в файл
                self.saveData()

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
                    self.saveData()
                else:
                    print("Удаление отменено")

    def showDateInfo(self):
        date = self.getDate()
        self.listView.clear()
        self.listView.setFixedWidth(401)

        pinned_notes = []
        regular_notes = []

        if date in self.data:
            for note in self.data[date]:
                decrypted_note = self.decrypt_data(note)
                if decrypted_note.startswith("📌"):
                    pinned_notes.append(decrypted_note)
                else:
                    regular_notes.append(decrypted_note)

            notes = pinned_notes + regular_notes

            self.data[date] = [self.encrypt_data(note) for note in notes]

            for note in notes:
                if ":" in note:
                    mainNote, additionalNote = note.split(":", 1)
                else:
                    mainNote, additionalNote = note, ""
                listItem, widget = createCustomListItem(str(mainNote), str(additionalNote))

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
        self.saveData()
        e.accept()

    def saveData(self):
        file_path = "/Users/maryday/Documents/reposgitmain/newrep-Uchebnaya-Praktika/data.json"
        with open(file_path, "w") as json_file:
            encrypted_data = {date: [self.encrypt_data(note) for note in notes] for date, notes in self.data.items()}
            json.dump(encrypted_data, json_file)

    def labelDate(self):
        select = self.calendarWidget.selectedDate()
        self.label_date.setLocale(QLocale(QLocale.Russian))
        weekday, month = select.dayOfWeek(), select.month()
        day, year = str(select.day()), str(select.year())
        russian_locale = QLocale(QLocale.Russian, QLocale.Russia)
        week_day = russian_locale.dayName(weekday)
        word_month = russian_locale.monthName(month)
        self.label_date.setText(week_day + ", " + day + ' ' + word_month + " " ", " + year)

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
        dialog.exec_()

    def highlightFirstItem(self):
        if self.listView.count() > 0:
            self.listView.setCurrentRow(0)

    def updateDateInfo(self):
        self.showDateInfo()

def createCustomListItem(mainNote, additionalNote, max_length=50):
    widget = QWidget()
    layout = QVBoxLayout(widget)

    mainNoteLabel = QLabel(mainNote)
    mainNoteLabel.setStyleSheet("font-family: Bahnschrift; font-size: 17px; font-weight: bold;")

    truncatedAdditionalNote = truncate_text(additionalNote, max_length)
    additionalNoteLabel = QLabel(truncatedAdditionalNote)
    additionalNoteLabel.setMaximumWidth(280)
    additionalNoteLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
    additionalNoteLabel.setStyleSheet("""
        font-family: Bahnschrift;
        font-size: 14px;
        color: black;
        white-space: nowrap;
        margin: 0;
        padding: 0;
    """)

    layout.addWidget(mainNoteLabel)
    layout.addWidget(additionalNoteLabel)

    listItem = QListWidgetItem()
    listItem.setData(Qt.UserRole, {"mainNote": mainNote, "additionalNote": additionalNote})
    listItem.setSizeHint(widget.sizeHint())

    return listItem, widget

def truncate_text(text, max_length=50):
    lines = text.splitlines()
    if not lines:
        return ""

    first_line = lines[0].strip()

    if len(lines) == 1 and len(first_line) <= max_length:
        return first_line

    if len(first_line.split()) > 1 and len(first_line) > max_length:
        return first_line[:max_length-3] + "..."

    return first_line[:max_length] + "..." if len(first_line) > max_length or len(lines) > 1 else first_line

def change_pass():
    dialog = PasswordDialog(is_first_time=True)
    if dialog.exec_() == QDialog.Accepted:
        user_password = dialog.get_password()
        if user_password:  # Only save if user entered a password
            save_password(user_password)
            msg = QtWidgets.QMessageBox()
            msg.setStyleSheet("QMessageBox {background-color: #FCF1C9}\n"
                              "QPushButton {\n"
                              "background-color: #F4DF96;\n"
                              "border-radius: 9%;\n"
                              "border: 1px solid gray;\n"
                              "width: 55px;\n"
                              "height: 25px;\n"
                              "}\n"
                              "QPushButton:hover {\n"
                              "background-color: #dbb44b;\n"
                              "}")
            msg.setText('Пароль успешно установлен!')
            msg.setWindowTitle('Успешно')
            msg.exec_()
        else:
            if path.exists(PASSWORD_FILE):
                with open(PASSWORD_FILE, 'w') as file:
                    json.dump({}, file)
            msg = QtWidgets.QMessageBox()
            msg.setStyleSheet("QMessageBox {background-color: #FCF1C9}\n"
                              "QPushButton {\n"
                              "background-color: #F4DF96;\n"
                              "border-radius: 9%;\n"
                              "border: 1px solid gray;\n"
                              "width: 55px;\n"
                              "height: 25px;\n"
                              "}\n"
                              "QPushButton:hover {\n"
                              "background-color: #dbb44b;\n"
                              "}")
            msg.setText('Пароль не установлен. Записи не будут защищены.')
            msg.setWindowTitle('Предупреждение')
            msg.exec_()
    else:
        msg = QtWidgets.QMessageBox()
        msg.setStyleSheet("QMessageBox {background-color: #FCF1C9}\n"
                              "QPushButton {\n"
                              "background-color: #F4DF96;\n"
                              "border-radius: 9%;\n"
                              "border: 1px solid gray;\n"
                              "width: 55px;\n"
                              "height: 25px;\n"
                              "}\n"
                              "QPushButton:hover {\n"
                              "background-color: #dbb44b;\n"
                              "}")
        msg.setText('Изменение пароля отменено')
        msg.setWindowTitle('Отмена')
        msg.exec_()

def main():
    app = QApplication(sys.argv)
    saved_password = load_password()
    attempts = 3
    if saved_password is None:
        dialog = PasswordDialog(is_first_time=True)
        if dialog.exec_() == QDialog.Accepted:
            user_password = dialog.get_password()
            if user_password:
                save_password(user_password)
                msg = QtWidgets.QMessageBox()
                msg.setStyleSheet("QMessageBox {background-color: #FCF1C9}\n"
                                "QPushButton {\n"
                                "background-color: #F4DF96;\n"
                                "border-radius: 9%;\n"
                                "border: 1px solid gray;\n"
                                "width: 55px;\n"
                                "height: 25px;\n"
                                "}\n"
                                "QPushButton:hover {\n"
                                "background-color: #dbb44b;\n"
                                "}")
                msg.setText('Пароль успешно установлен!')
                msg.setWindowTitle('Успешно')
                msg.exec_()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setStyleSheet("QMessageBox {background-color: #FCF1C9}\n"
                              "QPushButton {\n"
                              "background-color: #F4DF96;\n"
                              "border-radius: 9%;\n"
                              "border: 1px solid gray;\n"
                              "width: 55px;\n"
                              "height: 25px;\n"
                              "}\n"
                              "QPushButton:hover {\n"
                              "background-color: #dbb44b;\n"
                              "}")
                msg.setText('Пароль не установлен. Записи не будут защищены.')
                msg.setWindowTitle('Предупреждение')
                msg.exec_()
            run_main_app(app)
        else:
            sys.exit(0)
    else:
        while attempts > 0:
            dialog = PasswordDialog(is_first_time=False)
            if dialog.exec_() == QDialog.Accepted:
                user_password = dialog.get_password()
                if user_password and user_password == saved_password:
                    run_main_app(app)
                    return
                else:
                    attempts -= 1
                    msg = QtWidgets.QMessageBox()
                    msg.setStyleSheet("QMessageBox {background-color: #FCF1C9; height: 300px}\n"
                              "QPushButton {\n"
                              "background-color: #F4DF96;\n"
                              "border-radius: 9%;\n"
                              "border: 1px solid gray;\n"
                              "width: 55px;\n"
                              "height: 25px;\n"
                              "}\n"
                              "QPushButton:hover {\n"
                              "background-color: #dbb44b;\n"
                              "}")
                    msg.setText(f'Неправильный пароль. Осталось {attempts} попыток')
                    msg.setWindowTitle('Ошибка')
                    msg.exec_()
            else:
                sys.exit(0)

        if attempts == 0:
            clear_notes()
            msg = QtWidgets.QMessageBox()
            msg.setStyleSheet("QMessageBox {background-color: #FCF1C9; height: 300px}\n"
                        "QPushButton {\n"
                        "background-color: #F4DF96;\n"
                        "border-radius: 9%;\n"
                        "border: 1px solid gray;\n"
                        "width: 55px;\n"
                        "height: 25px;\n"
                        "}\n"
                        "QPushButton:hover {\n"
                        "background-color: #dbb44b;\n"
                        "}")
            msg.setText(f'Попытки закончились. Все ваши записи удалены')
            msg.setWindowTitle('Ошибка')
            msg.exec_()
            sys.exit(0)
            
def clear_notes():
    # Clear both notes and password data
    if path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as file:
            json.dump({}, file)

    if path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, 'w') as file:
            json.dump({}, file)

def run_main_app(app):
    russian_locale = QLocale(QLocale.Russian)
    QLocale.setDefault(russian_locale)
    planner = DailyPlanner()
    planner.show()
    app.exec()

if __name__ == "__main__":
    main()
