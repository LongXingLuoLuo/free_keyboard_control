import sys

from PyQt5 import QtWidgets

import auto_action
from pyUI import MainWindow


def test_main():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow(actionGroupDict=auto_action.readAllJsons())
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    test_main()
