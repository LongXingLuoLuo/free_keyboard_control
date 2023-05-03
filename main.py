import sys

from PyQt5.QtWidgets import QApplication

from auto_action import readAllJsons
from pyUI import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow(actionGroupDict=readAllJsons())
    win.show()
    sys.exit(app.exec())
