import datetime
import os.path
import sys

import pyautogui
import pynput.keyboard
from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtCore import Qt

from ui.transparent import Ui_transparentWidget

# 截图保存的文件夹
src_path = r'./images'
# 截图快捷键
screenShootKey = pynput.keyboard.Key.f8


def screenShootByKey():
    """
    按F8 开始截图，再按 F8 截图并保存, 保存名称为 %Y-%m-%d_%H-%M-%S.png
    :return:
    """

    def pressFirst(key):
        if key == screenShootKey:
            x1, y1 = pyautogui.position()

            def pressAgain(Key2):
                if Key2 == screenShootKey:
                    x2, y2 = pyautogui.position()
                    startX = x1 if x1 < x2 else x2
                    startY = y1 if y1 < y2 else y2
                    width = abs(x1 - x2)
                    height = abs(y1 - y2)
                    imgName = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.png'
                    if not os.path.exists(src_path):
                        # 如果src目录不存在则创建
                        os.mkdir(src_path)
                    pyautogui.screenshot(src_path + r'/' + imgName, region=(startX, startY, width, height))
                    return False

            # noinspection PyTypeChecker
            with pynput.keyboard.Listener(on_press=pressAgain) as listener2:
                listener2.join()
            return False

    # noinspection PyTypeChecker
    with pynput.keyboard.Listener(on_press=pressFirst) as listener:
        listener.join()


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


widgetPosition = QWidget()
ui_transparentWidget = Ui_transparentWidget()
ui_transparentWidget.setupUi(widgetPosition)


def showMousePosition():
    mousePosition = pyautogui.position()
    global widgetPosition
    widgetPosition.move(mousePosition.x, mousePosition.y)
    widgetPosition.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    showMousePosition()
    app.exec()
