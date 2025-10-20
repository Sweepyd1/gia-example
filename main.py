# main.py
import sys
from PyQt6.QtWidgets import QApplication
from db_manager import ensure_database_exists, import_xlsx_files_if_needed
from gui import DatabaseViewer


def main():
    ensure_database_exists()

    import_xlsx_files_if_needed()

    app = QApplication(sys.argv)
    window = DatabaseViewer()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
