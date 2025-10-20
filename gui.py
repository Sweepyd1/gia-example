from PyQt6.QtWidgets import (
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QPushButton,
    QLabel,
    QMessageBox,
)
from db_manager import get_table_data


class DatabaseViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Просмотрщик базы данных")
        self.resize(800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        layout.addWidget(QLabel("Имя таблицы:"))

        self.table_input = QLineEdit()
        self.table_input.setPlaceholderText("Введите имя таблицы")
        self.table_input.setFixedHeight(40)
        layout.addWidget(self.table_input)

        self.load_button = QPushButton("Загрузить данные")
        self.load_button.setFixedHeight(40)
        self.load_button.clicked.connect(self.load_table_data)
        layout.addWidget(self.load_button)

        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)

    def load_table_data(self):
        table_name = self.table_input.text().strip()
        if not table_name:
            QMessageBox.warning(self, "Ошибка", "Введите имя таблицы!")
            return

        try:
            columns, rows = get_table_data(table_name)
            self.display_data(columns, rows)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные:\n{e}")

    def display_data(self, columns, rows):
        self.table_widget.setRowCount(len(rows))
        self.table_widget.setColumnCount(len(columns))
        self.table_widget.setHorizontalHeaderLabels(columns)

        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(str(value) if value is not None else "NULL")
                self.table_widget.setItem(row_idx, col_idx, item)

        self.table_widget.resizeColumnsToContents()
