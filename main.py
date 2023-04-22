from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel

from utils import screenShotByKey


class MyWidget(QWidget):
    """实现全透明窗口"""

    def __init__(self):
        super(MyWidget, self).__init__()

        # 去除背景
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 窗口设置
        self.resize(320, 240)
        self.setWindowTitle('Test')
        self.setObjectName('MyWidget')
        self.setStyleSheet("QWidget#MyWidget{background:grey;}")

        # 添加个标签图片
        self.label = QLabel(self)
        self.label.setGeometry(120, 80, 66, 66)
        self.label.setText("(12, 28)")


if __name__ == '__main__':
    p = screenShotByKey()
    print(p)
