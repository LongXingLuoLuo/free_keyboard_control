# encoding = UTF-8
import os
import time

import pyautogui
import pyperclip


class ActionParamLackException(Exception):
    def __init__(self, value):
        super().__init__(value)
        self.value = value

    def __str__(self):
        return repr(self.value)


MOUSE_MOVETO = 0x00
MOUSE_MOVEREL = 0x01
MOUSE_CLICK = 0x02
MOUSE_DRAGTO = 0x03
MOUSE_DRAGREL = 0x04
KEYBOARD_KEY = 0x10
KEYBOARD_INPUT = 0x11
KEYBOARD_COPY = 0x12
TIME_DELAY = 0x20
ACTION_END = 0x30
COMMAND_RUN = 0x40
IMAGE_MOUSE_CLICK = 0x50
IMAGE_KEYBOARD_COPY = 0x51
IMAGE_WAIT = 0x52

# actionName_zh = {
#     COMMAND_RUN: '执行命令',
#     MOUSE_MOVETO: '移动鼠标到指定位置',
#     MOUSE_MOVEREL: '偏移鼠标',
#     MOUSE_CLICK: '鼠标点击'}
actionName_en = {
    MOUSE_MOVETO: 'MOUSE_MOVETO',
    MOUSE_MOVEREL: 'MOUSE_MOVEREL',
    MOUSE_CLICK: 'MOUSE_CLICK',
    MOUSE_DRAGTO: 'MOUSE_DRAGTO',
    MOUSE_DRAGREL: 'MOUSE_DRAGREL',
    KEYBOARD_KEY: 'KEYBOARD_KEY',
    KEYBOARD_INPUT: 'KEYBOARD_INPUT',
    KEYBOARD_COPY: 'KEYBOARD_COPY',
    TIME_DELAY: 'TIME_DELAY',
    ACTION_END: 'ACTION_END',
    COMMAND_RUN: 'COMMAND_RUN',
}


def generateFunc(data: dict):
    actionType = data['actionType']

    def func():
        pass

    if actionType == MOUSE_MOVETO:  # 鼠标指定移动
        x = data['x']
        x = data['y']

        def func():
            pyautogui.moveTo(x, y)
    elif actionType == MOUSE_MOVEREL:  # 鼠标偏移移动
        dx = data['dx']
        dy = data['dy']

        def func():
            pyautogui.moveRel(dx, dy)
    elif actionType == MOUSE_CLICK:  # 鼠标点击
        clickType = data['clickType']
        if 'x' in data.keys() and 'y' in data.keys():
            x = data['x']
            y = data['y']

            def func():
                pyautogui.click(button=clickType, x=x, y=y)
        else:
            def func():
                pyautogui.click(button=clickType)
    elif actionType == MOUSE_DRAGTO:  # 鼠标指定拖动
        x = data['x']
        y = data['y']

        def func():
            pyautogui.dragTo(x, y)
    elif actionType == MOUSE_DRAGREL:  # 鼠标偏移拖动

        def func():
            pyautogui.dragRel(data['dy'], data['dx'])
    elif actionType == KEYBOARD_KEY:  # 键盘快捷键
        key = data['key']

        def func():
            pyautogui.typewrite([key])
    elif actionType == KEYBOARD_INPUT:  # 键盘输入字符串
        string = data['string']

        if 'x' in data.keys() and 'y' in data.keys():
            x = data['x']
            y = data['y']

            def func():
                pyautogui.click(x, y)
                pyperclip.copy(string)
                pyautogui.hotkey('ctrl', 'v')
        else:
            def func():
                pyautogui.click()
                pyperclip.copy(string)
                pyautogui.hotkey('ctrl', 'v')
    elif actionType == KEYBOARD_COPY:  # 键盘复制屏幕上的字符串
        x = data['x']
        y = data['y']
        dx = data['dx']
        dy = data['dy']

        def func():
            pyautogui.click(x, y)
            pyautogui.dragRel(dx, dy)
            pyautogui.hotkey('ctrl', 'c')
    elif actionType == TIME_DELAY:
        dtime = data['dtime']

        def func():
            time.sleep(dtime)
    elif actionType == ACTION_END:
        def func():
            pass
    elif actionType == COMMAND_RUN:
        command = data['command']

        def func():
            os.system(command)
    return func


class ActionGroup(object):
    """动作组"""

    def __init__(self, dataList: list):
        super().__init__()
        self.dataList = dataList
        self.funcList = []
        for data in self.dataList:
            self.funcList.append(generateFunc(data))

    def run(self):
        """
        执行该动作组的全部动作
        :return:
        """
        for func in self.funcList:
            func()

    def append(self, __data):
        self.dataList.append(__data)
        self.funcList.append(generateFunc(__data))

    def insert(self, __index, __data):
        self.dataList.insert(__index, __data)
        self.funcList.insert(__index, generateFunc(__data))

    def pop(self, __index: int):
        self.dataList.pop(__index)
        self.funcList.pop(__index)

    def __str__(self):
        return str([actionName_en[data['actionType']] for data in self.dataList])

    def __repr__(self):
        return self.dataList

    def __len__(self):
        return len(self.dataList)

    def save(self, path):
        """
        保存为 json 文件
        :param path: 文件路径
        :return:
        """
        pass


def generateDict(actionType: int, **kwargs) -> None | dict:
    """
    根据参数生成字典
    MOUSE_MOVETO: x, y\n
    MOUSE_MOVEREL: dx, dy\n
    MOUSE_CLICK: clickType, (x, y)\n
    MOUSE_DRAGTO: x, y\n
    MOUSE_DRAGREL: dx, dy\n
    KEYBOARD_KEY: key:[]\n
    KEYBOARD_INPUT: string, (x, y)\n
    KEYBOARD_COPY: x, y, dx, dy\n
    TIME_DELAY: dtime\n
    ACTION_END: dtime\n
    COMMAND_RUN: command\n
    :param actionType: 动作类型
    :param kwargs: 动作的参数
    :return: 包含所有参数的字典
    """
    kwargs['actionType'] = actionType
    return kwargs


if __name__ == '__main__':
    ag = ActionGroup([])
    ag.append(generateDict(KEYBOARD_COPY, x=626, y=109, dx=20, dy=100))
    ag.run()
