import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QInputDialog
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QDateTime

class DailyJournalApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Daily Planner")
        self.setGeometry(100, 100, 500, 290)  

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

        self.edit_button = QPushButton("Редактировать запись", self) 
        self.edit_button.clicked.connect(self.edit_entry)

        self.read_button = QPushButton("Просмотреть записи", self)
        self.read_button.clicked.connect(self.read_entries)

        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.datetime_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.entry)
        layout.addWidget(self.save_button)
        layout.addWidget(self.clear_button)
        layout.addWidget(self.read_button)
        layout.addWidget(self.edit_button)

        self.update_datetime_label()

    def save_entry(self):
        text = self.entry.toPlainText().strip()
        if text:
            current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
            entry_with_time = f"{current_time}: {text}\n"
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
                entries_text = [entry.strip() for entry in entries]
                dialog = QInputDialog()
                chosen_entry, ok = dialog.getItem(self, "Выберите запись", "Записи:", entries_text, 0, False)
                if ok:
                    self.edit_chosen_entry(chosen_entry)
                else:
                    QMessageBox.information(self, "Записи", "Нет сохраненных записей.")
        except FileNotFoundError:
            QMessageBox.information(self, "Ошибка", "Файл с записями не найден.")
        except Exception as e: 
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def edit_chosen_entry(self, chosen_entry):
        datetime_created, entry_text = chosen_entry.split(':', 1)
        self.entry.setPlainText(f"{datetime_created}\n{entry_text}")

    def save_edited_entry(self, chosen_entry_index, new_entry_text):
        all_entries = []
        with open("daily_journal.txt", "r") as file:
            all_entries = file.readlines()

        all_entries[chosen_entry_index] = new_entry_text

        with open("daily_journal.txt", "w") as file:
            for entry in all_entries:
                file.write(entry)

    def edit_entry(self):
        try:
            with open("dailyjournal.txt", "r") as file:
                entries = file.readlines()
            if entries:
                last_entry = entries[-1]
                text_parts = last_entry.split('\n')
                if len(text_parts) > 1:
                    self.entry.setPlainText('\n'.join(text_parts[1:]))
                else:
                    QMessageBox.information(self, "Записи", "Нет текста для редактирования в последней записи")
            else:
                QMessageBox.information(self,"Записи", "Нет сохраненных записей для редактирования")
        except FileNotFoundError:
            QMessageBox.information(self, "Записи", "Нет сохраненных записей для редактирования")
            
    def update_datetime_label(self):
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm")
        self.datetime_label.setText(current_time)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DailyJournalApp()
    window.update_datetime_label()
    window.show()
    sys.exit(app.exec())