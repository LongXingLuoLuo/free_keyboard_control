# encoding = UTF-8
import json
import os
import time

import keyboard
import pyautogui
import pyperclip

from log_config import logger
from utils import getAllFiles

# 动作组数据的保存文件夹
datasDir = './datas'
# ! pyautogui 函数执行间隔
pyautogui.PAUSE = 0.5
# ! 动作执行间隔时间
ACTION_PAUSE = 0.1
# ! 在长时间动作中，结束动作运行
stopKey = '`'

# * 动作类型
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
IMAGE_MOVE = 'IMAGE_MOVE'


class ActionKeyLackException(Exception):
    def __init__(self, value):
        super().__init__(value)
        self.value = value

    def __str__(self):
        return repr(self.value)


actionTypeName = {
    MOUSE_MOVETO: '鼠标移动到指定位置',
    MOUSE_MOVEREL: '鼠标移动距离',
    MOUSE_CLICK: '鼠标点击',
    MOUSE_DRAGTO: '鼠标拖动到指定位置',
    MOUSE_DRAGREL: '鼠标拖动量',
    KEYBOARD_KEY: '模拟按键点击',
    KEYBOARD_INPUT: '输入文本',
    KEYBOARD_COPY: '复制区域内文本',
    TIME_DELAY: '延时',
    ACTION_END: '结束执行',
    COMMAND_RUN: '运行cmd命令',
    IMAGE_MOUSE_CLICK: '点击屏幕上所有指定图片',
    IMAGE_WAIT: '等待直到屏幕上出现指定图片',
    IMAGE_SCREENSHOT: '截图',
    IMAGE_MOVE: '鼠标移动到指定图片位置',
}

clickTypeName = {
    'left': '左键',
    'middle': '中键',
    'right': '右键',
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

    explain = ""
    if actionType == MOUSE_MOVETO:  # 鼠标指定移动
        x, y = data['pos']

        def func():
            """鼠标指定移动"""
            pyautogui.moveTo(x, y)
            return True

        explain = f"鼠标移动到({x}, {y})"
    elif actionType == MOUSE_MOVEREL:  # 鼠标偏移移动
        x, y = data['pos']

        def func():
            """鼠标偏移移动"""
            pyautogui.moveRel(x, y)
            return True

        explain = f"鼠标偏移移动({x}, {y})"
    elif actionType == MOUSE_CLICK:  # 鼠标点击
        clickType = data.get('clickType', 'left')
        x, y = data['pos']

        def func():
            """鼠标点击"""
            pyautogui.click(button=clickType, x=x, y=y)
            return True

        explain = f"在({x}, {y})鼠标点击({clickType})"
    elif actionType == MOUSE_DRAGTO:  # 鼠标指定拖动
        x, y = data['pos']

        def func():
            """鼠标指定拖动"""
            pyautogui.dragTo(x, y)
            return True

        explain = f"鼠标拖动到({x}, {y})"
    elif actionType == MOUSE_DRAGREL:  # 鼠标偏移拖动
        x, y = data['pos']

        def func():
            """鼠标偏移拖动"""
            pyautogui.dragRel(x, y)
            return True

        explain = f"鼠标偏移拖动({x}, {y})"
    elif actionType == KEYBOARD_KEY:  # 键盘快捷键
        key = data['key']

        def func():
            """键盘快捷键"""
            pyautogui.hotkey(*key)
            return True

        explain = f"模拟按下({'+'.join(key)})"
    elif actionType == KEYBOARD_INPUT:  # 键盘输入字符串
        inputStr = data['inputStr']

        def func():
            """键盘输入字符串"""
            pyautogui.click()
            pyperclip.copy(inputStr)
            pyautogui.hotkey('ctrl', 'v')
            return True

        explain = f"输入字符串{inputStr}"
    elif actionType == KEYBOARD_COPY:  # 复制区域内的字符串
        x, y, dx, dy = data['region']

        def func():
            """复制区域内的字符串"""
            pyautogui.click(x, y)
            pyautogui.dragRel(dx, dy)
            pyautogui.hotkey('ctrl', 'c')
            return True

        explain = f"复制({x}, {y}, {dx}, {dy})区域内的字符串"
    elif actionType == TIME_DELAY:  # 延时
        mtime = data['mtime']

        def func():
            """延时"""
            t1 = time.time()
            while time.time() < t1 + mtime:
                if keyboard.is_pressed(stopKey):
                    return False
                time.sleep(1)
            return True

        explain = f"延时 {mtime}s"
    elif actionType == ACTION_END:  # 结束动作
        mtime = data['mtime']

        def func():
            """结束动作"""
            t1 = time.time()
            while time.time() < t1 + mtime:
                if keyboard.is_pressed(stopKey):
                    return False
                time.sleep(1)
            return False

        explain = f"{mtime}s 后结束"
    elif actionType == COMMAND_RUN:  # 运行命令
        inputStr = data['inputStr']

        def func():
            """运行命令"""
            os.system(inputStr)
            return True

        explain = f"运行 {inputStr}"
    elif actionType == IMAGE_MOUSE_CLICK:  # 检测到图片后点击
        path = data['path']
        clickType = data['clickType']
        region = data['region']

        def func():
            """检测到图片后点击"""
            if not os.path.exists(path):
                return False
            boxes = pyautogui.locateAllOnScreen(path, region=region)
            for box in boxes:
                pyautogui.click(box.left + box.width / 2, box.top + box.height / 2, button=clickType)
                print(box)
            return True

        explain = f"检测{region}区域内点击({clickType}) {path}"
    elif actionType == IMAGE_WAIT:  # 直到检测到图片后执行
        path = data['path']
        mtime = data.get('mtime', 1000)

        def func():
            t1 = time.time()
            while pyautogui.locateOnScreen(path) is None:
                if time.time() > t1 + mtime:
                    return False
                elif keyboard.is_pressed(stopKey):
                    return False
                else:
                    time.sleep(0.05)
            return True

        explain = f"在 {mtime}s 内检测是否有 {path}"
    elif actionType == IMAGE_SCREENSHOT:  # 截图
        path = data['path']
        region = data['region']

        def func():
            pyautogui.screenshot(path, region=region)
            return True

        explain = f"在{region}区域内截图，保存为 {path}"
    elif actionType == IMAGE_MOVE:  # 鼠标移动到指定图片位置
        path = data['path']

        def func():
            box = pyautogui.locateOnScreen(path)
            if box is None:
                return False
            pyautogui.moveTo(box.left + box.width / 2, box.top + box.height / 2)
            return True

        explain = f"鼠标移动到 {os.path.basename(path)}"
    return func, explain


class ActionGroup(object):
    """动作组"""

    def __init__(self, name: str, dataList: None | list[dict[str, str | int]] = None):
        super().__init__()
        if dataList is None:
            dataList = []
        self.name = name
        self.TAG = f"ActionGroup[{self.name}]"
        self.funcList = []
        self.explainList = []
        self.dataList = dataList
        for data in self.dataList:
            try:
                func, explain = generateFunc(data)
                self.funcList.append(func)
                self.explainList.append(explain)
            except KeyError:
                logger.error(f"{self.TAG}: KeyError in dataList({dataList})")


    def run(self):
        """
        执行该动作组的全部动作
        :return: 是否运行成功
        """
        logger.info(self.TAG + ": running...")
        try:
            for i, func in enumerate(self.funcList):
                logger.debug(self.TAG + f": run {self.dataList[i]}.")
                if not func():
                    logger.info(self.TAG + ": run end.")
                    return False
                time.sleep(ACTION_PAUSE)
        except OSError:
            logger.error(self.TAG + ": run error.")
        logger.info(self.TAG + ": run end.")
        return True

    def append(self, __data: dict[str, str | int]):
        """
        从末尾添加
        :param __data:
        :return:
        """
        self.dataList.append(__data)
        func, explain = generateFunc(__data)
        self.funcList.append(func)
        self.explainList.append(explain)
        logger.debug(self.TAG + f": append {__data}.")

    def insert(self, __index: int, __data: dict[str, str | int]):
        """
        在指定下标插入新动作
        :param __index:
        :param __data:
        :return:
        """
        self.dataList.insert(__index, __data)
        func, explain = generateFunc(__data)
        self.funcList.insert(__index, func)
        self.explainList.insert(__index, explain)
        logger.debug(self.TAG + f": insert ({__index}) {__data}.")

    def pop(self, __index: int):
        """
        弹出指定下标的数据
        :param __index:
        :return:
        """
        self.dataList.pop(__index)
        self.funcList.pop(__index)
        self.explainList.pop(__index)
        logger.debug(self.TAG + f": pop {__index}.")

    def swap(self, index1: int, index2: int):
        if index1 == index2:
            return
        size = len(self)
        if 0 <= index1 < size and 0 <= index2 < size:
            self.dataList[index1], self.dataList[index2] = self.dataList[index2], self.dataList[index1]
            self.funcList[index1], self.funcList[index2] = self.funcList[index2], self.funcList[index1]
            self.explainList[index1], self.explainList[index2] = self.explainList[index2], self.explainList[index1]

    def __str__(self):
        return str(self.explainList)

    def __repr__(self):
        return self.dataList

    def __len__(self):
        return len(self.dataList)

    def __bool__(self):
        return len(self) != 0

    def __iter__(self):
        return self.dataList.__iter__()

    def clear(self):
        self.dataList = []
        self.funcList = []
        logger.debug(self.TAG + ": clear")

    def json(self) -> str:
        """
        返回json 类型
        :return:
        """
        return json.dumps(self.dataList)

    def getPath(self) -> str:
        """
        返回所保存的文件路径
        :return: 所保存的文件路径
        """
        if not os.path.isdir(datasDir):
            os.mkdir(datasDir)
        path = os.path.abspath(datasDir + '\\' + self.name + '.json')
        return path

    def save(self):
        """
        保存为 json 文件
        :return:
        """

        with open(self.getPath(), encoding='UTF-8', mode='w') as f:
            f.write(self.json())
            logger.debug(f"ActionGroup[{self.name}] : saved in {self.getPath()}.")

    def deleteFile(self):
        os.remove(self.getPath())
        self.clear()
        logger.info(f"ActionGroup[{self.name}] : delete {self.getPath()}")

    # def read(self, path):
    #     jsonData = json.loads(open(path, encoding='UTF-8'))


def generateAction(actionType: str, **kwargs) -> None | dict[str, str | int]:
    """
    根据参数生成字典
    MOUSE_MOVETO: pos\n
    MOUSE_MOVEREL: pos\n
    MOUSE_CLICK: pos, clickType\n
    MOUSE_DRAGTO: pos\n
    MOUSE_DRAGREL: pos\n
    KEYBOARD_KEY: key:[]\n
    KEYBOARD_INPUT: inputStr\n
    KEYBOARD_COPY: region\n
    TIME_DELAY: mtime\n
    ACTION_END: mtime\n
    COMMAND_RUN: inputStr\n
    IMAGE_MOUSE_CLICK: path, clickType, region\n
    IMAGE_WAIT: path, mtime\n
    IMAGE_SCREENSHOT: path, region, mtime\n
    IMAGE_MOVE path, region, mtime\n
    :param actionType: 动作类型
    :param kwargs: 动作的参数
    :return: 包含所有参数的字典
    """
    kwargs['actionType'] = actionType
    return kwargs


def readAllJsons() -> dict[str, ActionGroup]:
    files = getAllFiles(datasDir, '.json$')
    actionGroupDict = {}
    for path in files:
        name = str(os.path.basename(path))
        name = name[:-5]
        with open(path, 'r') as f:
            actionGroup = ActionGroup(name=name, dataList=json.load(f))
            actionGroupDict[name] = actionGroup
    return actionGroupDict


if __name__ == '__main__':
    for k, v in readAllJsons().items():
        print(v.__repr__())
