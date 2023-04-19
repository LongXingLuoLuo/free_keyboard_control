# encoding = UTF-8
import json
import os
import time

import pyautogui
import pyperclip

pyautogui.PAUSE = 0.5


class ActionKeyLackException(Exception):
    def __init__(self, value):
        super().__init__(value)
        self.value = value

    def __str__(self):
        return repr(self.value)


# ! 动作执行间隔时间
ACTION_PAUSE = 0.01

MOUSE_MOVETO = 'MOUSE_MOVETO'
MOUSE_MOVEREL = 'MOUSE_MOVEREL'
MOUSE_CLICK = 'MOUSE_CLICK'
MOUSE_DRAGTO = 'MOUSE_DRAGTO'
MOUSE_DRAGREL = 'MOUSE_DRAGREL'
KEYBOARD_KEY = 'KEYBOARD_KEY'
KEYBOARD_INPUT = 'KEYBOARD_INPUT'
KEYBOARD_COPY = 'KEYBOARD_COPY'
TIME_DELAY = 'TIME_DELAY'
ACTION_END = 'ACTION_END'
COMMAND_RUN = 'COMMAND_RUN'
IMAGE_MOUSE_CLICK = 'IMAGE_MOUSE_CLICK'
IMAGE_WAIT = 'IMAGE_WAIT'
IMAGE_SCREENSHOT = 'IMAGE_SCREENSHOT'
IMAGE_WAIT_CLICK = 'IMAGE_WAIT_CLICK'

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
    IMAGE_MOUSE_CLICK: 'IMAGE_MOUSE_CLICK',
    IMAGE_WAIT: 'IMAGE_WAIT',
    IMAGE_SCREENSHOT: 'IMAGE_SCREENSHOT',
    IMAGE_WAIT_CLICK: 'IMAGE_WAIT_CLICK',
}


def generateFunc(data: dict):
    """
    生成动作函数
    :param data:
    :return:
    """
    actionType = data['actionType']

    def func():
        """默认函数"""
        return False

    if actionType == MOUSE_MOVETO:  # 鼠标指定移动
        x = data['x']
        x = data['y']

        def func():
            """鼠标指定移动"""
            pyautogui.moveTo(x, y)
            return True
    elif actionType == MOUSE_MOVEREL:  # 鼠标偏移移动
        dx = data['dx']
        dy = data['dy']

        def func():
            """鼠标偏移移动"""
            pyautogui.moveRel(dx, dy)
            return True
    elif actionType == MOUSE_CLICK:  # 鼠标点击
        clickType = data.get('clickType', 'left')
        if 'x' in data.keys() and 'y' in data.keys():
            x = data['x']
            y = data['y']

            def func():
                """鼠标点击"""
                pyautogui.click(button=clickType, x=x, y=y)
                return True
        else:
            def func():
                """鼠标点击"""
                pyautogui.click(button=clickType)
                return True
    elif actionType == MOUSE_DRAGTO:  # 鼠标指定拖动
        x = data['x']
        y = data['y']

        def func():
            """鼠标指定拖动"""
            pyautogui.dragTo(x, y)
            return True
    elif actionType == MOUSE_DRAGREL:  # 鼠标偏移拖动

        def func():
            """鼠标偏移拖动"""
            pyautogui.dragRel(data['dy'], data['dx'])
            return True
    elif actionType == KEYBOARD_KEY:  # 键盘快捷键
        key = data['key']

        def func():
            """键盘快捷键"""
            pyautogui.typewrite([key])
            return True
    elif actionType == KEYBOARD_INPUT:  # 键盘输入字符串
        string = data['string']

        if 'x' in data.keys() and 'y' in data.keys():
            x = data['x']
            y = data['y']

            def func():
                """键盘输入字符串"""
                pyautogui.click(x, y)
                pyperclip.copy(string)
                pyautogui.hotkey('ctrl', 'v')
                return True
        else:
            def func():
                """键盘输入字符串"""
                pyautogui.click()
                pyperclip.copy(string)
                pyautogui.hotkey('ctrl', 'v')
                return True
    elif actionType == KEYBOARD_COPY:  # 复制区域内的字符串
        x = data['x']
        y = data['y']
        dx = data['dx']
        dy = data['dy']

        def func():
            """复制区域内的字符串"""
            pyautogui.click(x, y)
            pyautogui.dragRel(dx, dy)
            pyautogui.hotkey('ctrl', 'c')
            return True
    elif actionType == TIME_DELAY:  # 延时
        dtime = data['dtime']

        def func():
            """延时"""
            time.sleep(dtime)
            return True
    elif actionType == ACTION_END:  # 结束动作
        def func():
            """结束动作"""
            return False
    elif actionType == COMMAND_RUN:  # 运行命令
        command = data['command']

        def func():
            """运行命令"""
            os.system(command)
            return True
    elif actionType == IMAGE_MOUSE_CLICK:       # 检测到图片后点击
        path = data['path']
        clickType = data.get('clickType', 'left')
        if 'x' in data.keys() and 'y' in data.keys() and 'dx' in data.keys() and 'dy' in data.keys():
            x = data['x']
            y = data['y']
            dx = data['dx']
            dy = data['dy']

            def func():
                """检测到图片后点击"""
                boxes = pyautogui.locateAllOnScreen(path)
                for box in boxes:
                    pyautogui.click(box.left + box.width / 2, box.top + box.height / 2, button=clickType,
                                    region=(x, y, dx, dy))
                return True
        else:
            def func():
                """检测到图片后点击"""
                boxes = pyautogui.locateAllOnScreen(path)
                for box in boxes:
                    pyautogui.click(box.left + box.width / 2, box.top + box.height / 2, button=clickType)
                return True
    elif actionType == IMAGE_WAIT:
        path = data['path']
        mtime = data.get('mtime', 1000)

        def func():
            t1 = time.time()
            while pyautogui.locateOnScreen(path) is None:
                if time.time() > t1 + mtime:
                    return False
                else:
                    time.sleep(0.05)
            return True
    elif actionType == IMAGE_SCREENSHOT:
        path = data['path']
        if 'x' in data.keys() and 'y' in data.keys() and 'dx' in data.keys() and 'dy' in data.keys():
            x = data['x']
            y = data['y']
            dx = data['dx']
            dy = data['dy']

            def func():
                pyautogui.screenshot(path, region=(x, y, dx, dy))
                return True
        else:
            def func():
                pyautogui.screenshot(path)
                return True
    elif actionType == IMAGE_WAIT_CLICK:
        path = data['path']
        mtime = data.get('mtime', 1000)
        clickType = data.get('clickType', 'left')
        if 'x' in data.keys() and 'y' in data.keys() and 'dx' in data.keys() and 'dy' in data.keys():
            x = data['x']
            y = data['y']
            dx = data['dx']
            dy = data['dy']

            def func():
                t1 = time.time()
                while pyautogui.locateOnScreen(path, region=(x, y, dx, dy)) is None:
                    if time.time() > t1 + mtime:
                        return False
                    else:
                        time.sleep(0.05)
                box = pyautogui.locateOnScreen(path)
                pyautogui.click(box.left + box.width / 2, box.top + box.height / 2, button=clickType)
                return True
        else:
            def func():
                t1 = time.time()
                while pyautogui.locateOnScreen(path) is None:
                    if time.time() > t1 + mtime:
                        return False
                    else:
                        time.sleep(0.05)
                box = pyautogui.locateOnScreen(path)
                pyautogui.click(box.left + box.width / 2, box.top + box.height / 2, button=clickType)
                return True
    return func


class ActionGroup(object):
    """动作组"""

    def __init__(self, dataList: list):
        super().__init__()
        self.dataList = dataList
        self.funcList = [generateFunc(data) for data in self.dataList]

    def run(self):
        """
        执行该动作组的全部动作
        :return: 是否运行成功
        """
        for func in self.funcList:
            if not func():
                return False
            time.sleep(ACTION_PAUSE)
        return True

    def append(self, __data):
        """
        从末尾添加
        :param __data:
        :return:
        """
        self.dataList.append(__data)
        self.funcList.append(generateFunc(__data))

    def insert(self, __index, __data):
        """
        在指定下标插入新动作
        :param __index:
        :param __data:
        :return:
        """
        self.dataList.insert(__index, __data)
        self.funcList.insert(__index, generateFunc(__data))

    def pop(self, __index: int):
        """
        弹出指定下标的数据
        :param __index:
        :return:
        """
        self.dataList.pop(__index)
        self.funcList.pop(__index)

    def __str__(self):
        return str([actionName_en[data['actionType']] for data in self.dataList])

    def __repr__(self):
        return self.dataList

    def __len__(self):
        return len(self.dataList)

    def __bool__(self):
        return len(self) != 0

    def __iter__(self):
        return self.dataList.__iter__()

    def json(self):
        """
        返回json 类型
        :return:
        """
        return json.dumps(self.dataList)

    def save(self, path):
        """
        保存为 json 文件
        :param path: 文件路径
        :return:
        """
        with open(path, encoding='UTF-8', mode='w') as f:
            f.write(self.json())

    # def read(self, path):
    #     jsonData = json.loads(open(path, encoding='UTF-8'))


def generateActionDict(actionType: str, **kwargs) -> None | dict:
    """
    根据参数生成字典
    MOUSE_MOVETO: x, y\n
    MOUSE_MOVEREL: dx, dy\n
    MOUSE_CLICK: (x, y, clickType)\n
    MOUSE_DRAGTO: x, y\n
    MOUSE_DRAGREL: dx, dy\n
    KEYBOARD_KEY: key:[]\n
    KEYBOARD_INPUT: string, (x, y)\n
    KEYBOARD_COPY: x, y, dx, dy\n
    TIME_DELAY: dtime\n
    ACTION_END: dtime\n
    COMMAND_RUN: command\n
    IMAGE_MOUSE_CLICK: path, (clickType, x, y, dx, dy)\n
    IMAGE_WAIT: path, mtime\n
    IMAGE_SCREENSHOT: path, (x, y, dx, dy, mtime)\n
    IMAGE_WAIT_CLICK: path, (x, y, dx, dy, mtime)\n
    :param actionType: 动作类型
    :param kwargs: 动作的参数
    :return: 包含所有参数的字典
    """
    kwargs['actionType'] = actionType
    return kwargs


if __name__ == '__main__':
    ag = ActionGroup([])
    ag.append(generateActionDict(actionType=IMAGE_WAIT_CLICK, path='./images/2023-04-19_22-37-05.png', mtime=40000))
    print(ag.run())
