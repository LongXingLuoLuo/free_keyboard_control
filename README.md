# 自由鼠标控制

## 项目说明

该项目是可视化制定鼠标控制，
功能包括，在指定位置点击，拖动，根据图片点击全部，复制某一区域内的全部文本到剪贴板

## 需求

### 功能需求

+ [X]  鼠标左击/右击
  + [X]  左点击
  + [X]  右点击
+ [X]  鼠标移动到指定位置
  + [X]  偏差移动
  + [ ]  固定位置（F1 确认）
+ [ ]  延时时间
  + [ ]  延时后执行
+ [ ]  结束任务
+ [ ]  运行 cmd 指令
+ [ ]  自动、手动结束运行
  + [X]  快捷键结束运行
  + [ ]  长时间运行后自动结束运行（安全）

### UI 需求

+ [X]  用户添加指定名字的动作组
+ [ ]  添加动作
+ [ ]  可以拖动改变动作顺序
+ [ ]  通过按键读取鼠标位置
+ [ ]  通过按键获取指定区域

### 添加新动作界面

```
MOUSE_MOVETO: pos\n
MOUSE_MOVEREL: pos\n
MOUSE_CLICK: (pos, clickType)\n
MOUSE_DRAGTO: pos\n
MOUSE_DRAGREL: pos\n
KEYBOARD_KEY: key:[]\n
KEYBOARD_INPUT: inputStr, (pos)\n
KEYBOARD_COPY: region\n
TIME_DELAY: mtime\n
ACTION_END: mtime\n
COMMAND_RUN: inputStr\n
IMAGE_MOUSE_CLICK: path, (clickType, region)\n
IMAGE_WAIT: path, mtime\n
IMAGE_SCREENSHOT: path, (region, mtime)\n
IMAGE_WAIT_CLICK: path, (region, mtime)\n
```
坐标 pos: (x, y)
区域 region: (left, top, width, height)
点击类型 clickType[left, right, middle]
按键 key: []
输入文本 inputStr
最大时间 mtime: float
图片路径 path: filepath
