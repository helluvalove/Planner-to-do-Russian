import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QDateTime

class DailyJournalApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ежедневник")
        self.setGeometry(100, 100, 500, 300)  # Начальные размеры окна

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.init_ui()

    def init_ui(self):
        self.datetime_label = QLabel("", self)
        font = QFont("Arial", 14)
        font.setBold(True)
        self.datetime_label.setFont(font)

        self.title_label = QLabel("Добавить запись:", self)
        font = QFont("Arial", 14)
        font.setBold(True)
        self.title_label.setFont(font)

        self.entry = QTextEdit(self)
        font = QFont("Arial", 12)
        self.entry.setFont(font)

        self.save_button = QPushButton("Сохранить", self)
        self.save_button.clicked.connect(self.save_entry)

        self.clear_button = QPushButton("Очистить", self)
        self.clear_button.clicked.connect(self.clear_entry)

        self.read_button = QPushButton("Просмотреть записи", self)
        self.read_button.clicked.connect(self.read_entries)

        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.datetime_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.entry)
        layout.addWidget(self.save_button)
        layout.addWidget(self.clear_button)
        layout.addWidget(self.read_button)

        self.update_datetime_label()

    def save_entry(self):
        text = self.entry.toPlainText().strip()
        if text:
            current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
            entry_with_time = f"{current_time}\n{text}\n"
            with open("daily_journal.txt", "a") as file:
                file.write(entry_with_time)
            QMessageBox.information(self, "Успешно", "Запись сохранена успешно.")
            self.clear_entry()
        else:
            QMessageBox.warning(self, "Пустая запись", "Введите текст записи перед сохранением.")

    def clear_entry(self):
        self.entry.clear()

    def read_entries(self):
        try:
            with open("daily_journal.txt", "r") as file:
                entries = file.readlines()
            if entries:
                entries_text = "\n".join(entries)
                QMessageBox.information(self, "Записи", entries_text)
            else:
                QMessageBox.information(self, "Записи", "Нет сохраненных записей.")
        except FileNotFoundError:
            QMessageBox.information(self, "Записи", "Нет сохраненных записей.")

    def update_datetime_label(self):
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm")
        self.datetime_label.setText(current_time)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DailyJournalApp()
    window.show()
    sys.exit(app.exec())