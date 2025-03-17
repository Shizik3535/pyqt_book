import sys

from PyQt6.QtWidgets import QApplication
from qt_material import apply_stylesheet

from app.ui.main_window import MainWindow
# from app.ui.auth_window import AuthWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # auth_window = AuthWindow()
    # auth_window.show()
    main_window = MainWindow()
    main_window.show()

    apply_stylesheet(app, theme="dark_blue.xml")

    sys.exit(app.exec())
