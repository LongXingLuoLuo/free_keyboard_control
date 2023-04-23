import datetime
import os
import re
import time

import pyautogui
import pynput.keyboard

# 截图保存的文件夹
imagesPath = r'./images'
# 截图快捷键, 默认为 F8
positionKey = pynput.keyboard.Key.f8
mtime = 600


def getPositionByKey():
    """
    按下按键f8后返回鼠标位置
    :return:
    """

    def on_press(key):
        return key != positionKey

    def daemon():
        t1 = time.time()
        while time.time() < t1 + mtime:
            time.sleep(1)
        return False

    with pynput.keyboard.Listener(on_press=on_press, daemon=daemon) as h:
        h.join()
    x, y = pyautogui.position()
    return x, y


def getBoxByKey():
    """
    开内需两次按下 positionKey , 获取所选区域的 box
    :return: Box(left, top, width, height)
    """
    x1, y1 = getPositionByKey()
    x2, y2 = getPositionByKey()
    left = x1 if x1 < x2 else x2
    top = y1 if y1 < y2 else y2
    width = abs(x1 - x2)
    height = abs(y1 - y2)
    return left, top, width, height


def nowTime():
    """
    返回当前时间的 %Y-%m-%d_%H-%M-%S 格式
    :return:
    """
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def screenShotByKey():
    """
    按下两次快捷键后截图, 保存名称为 %Y-%m-%d_%H-%M-%S.png
    :return: 文件保存地址
    """
    imgName = nowTime() + '.png'
    path = os.path.abspath(imagesPath + r'/' + imgName)
    if not os.path.exists(imagesPath):
        # 如果src目录不存在则创建
        os.mkdir(imagesPath)
    pyautogui.screenshot(path, region=getBoxByKey())
    return path


def getAllFiles(rootPath: str, expression: str) -> list:
    """
    获取根目录下的所有文件列表
    :param rootPath: 根目录
    :param expression: 文件名正则表达式
    :return: 根目录下的所有文件列表
    """
    if not os.path.exists(rootPath):
        return []
    allFiles = []
    cp = re.compile(expression)
    for filename in os.listdir(rootPath):
        path = os.path.join(rootPath, filename)
        if os.path.isdir(path):
            allFiles += getAllFiles(path)
        elif cp.search(path):
            allFiles.append(os.path.abspath(path))
    return allFiles
