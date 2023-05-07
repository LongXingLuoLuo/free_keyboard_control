# -*- coding:UTF-8 -*-
import json
import os.path
import re

import PIL.Image
import pyperclip
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot, QPoint, QModelIndex

import auto_action
import utils
from log_config import logger


class AuthorWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AuthorWidget, self).__init__(parent)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.textBrowser = QtWidgets.QTextBrowser(self)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("authorWidget")
        self.resize(534, 419)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("authorWidget", "作者介绍"))
        self.textBrowser.setHtml(_translate("authorWidget",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><title>作者介绍</title><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                            "<h2 style=\" margin-top:16px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"软件介绍\"></a><span style=\" font-size:x-large; font-weight:600;\">软</span><span style=\" font-size:x-large; font-weight:600;\">件介绍</span></h2>\n"
                                            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">该软件是用来可视化自定义键鼠控制，实现自动化操作。</span></p>\n"
                                            "<h2 style=\" margin-top:16px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"作者个人网站\"></a><span style=\" font-size:x-large; font-weight:600;\">作</span><span style=\" font-size:x-large; font-weight:600;\">者个人网站</span></h2>\n"
                                            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://github.com/LongXingLuoLuo\"><span style=\" text-decoration: underline; color:#0000ff;\">https://github.com/LongXingLuoLuo</span></a></p>\n"
                                            "<h2 style=\" margin-top:16px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:x-large; font-weight:600;\">软件 github 仓库</span></h2>\n"
                                            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://github.com/LongXingLuoLuo/free_keyboard_control\"><span style=\" text-decoration: underline; color:#0000ff;\">https://github.com/LongXingLuoLuo/free_keyboard_control</span></a></p>\n"
                                            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">（若该链接进不去，则说明作者本人未公开此仓库。）</p>\n"
                                            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:600;\">截图功能使用 </span></p>\n"
                                            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">点击“截图”，然后在需要截图的区域的左上角和右下角分别按下 F8，即完成截图，截图保存在软件目录下 <span style=\" font-weight:600;\">images </span>文件夹下。</p>\n"
                                            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:600;\">坐标和选区功能使用</span></p>\n"
                                            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">把鼠标移动到在想要选的坐标下，然后按下 F8，即可选择该坐标。</p>\n"
                                            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">在选择的区域的左上角和右下角分别按下 F8，即选择矩形区域。</p></body></html>"))


class ActionGroupNameDialog(QtWidgets.QDialog):

    def __init__(self, parent: QtWidgets.QMainWindow = None):
        super(ActionGroupNameDialog, self).__init__(parent)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.label = QtWidgets.QLabel(self)
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("ActionGroupNameDialog")
        self.resize(387, 117)
        self.verticalLayout.setObjectName("verticalLayout")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)  # type: ignore
        self.buttonBox.rejected.connect(self.reject)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("ActionGroupNameDialog", "新动作组名字"))
        self.label.setText(_translate("ActionGroupNameDialog", "输入要添加的新动作组名字："))

    def getInput(self) -> str:
        return self.lineEdit.text().strip()


class ActionDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ActionDialog, self).__init__(parent)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.actionTypeHLayout = QtWidgets.QHBoxLayout()
        self.actionTypeLabel = QtWidgets.QLabel(self)
        self.actionTypeComboBox = QtWidgets.QComboBox(self)
        self.posHLayout = QtWidgets.QHBoxLayout()
        self.posLabel = QtWidgets.QLabel(self)
        self.posLineEdit = QtWidgets.QLineEdit(self)
        self.posBtn = QtWidgets.QPushButton(self)
        self.regionHLayout = QtWidgets.QHBoxLayout()
        self.regionLabel = QtWidgets.QLabel(self)
        self.regionLineEdit = QtWidgets.QLineEdit(self)
        self.regionBtn = QtWidgets.QPushButton(self)
        self.clickTypeHLayout = QtWidgets.QHBoxLayout()
        self.clickTypeLabel = QtWidgets.QLabel(self)
        self.clickTypeComboBox = QtWidgets.QComboBox(self)
        self.keyHLayout = QtWidgets.QHBoxLayout()
        self.keySequenceEdit = QtWidgets.QKeySequenceEdit(self)
        self.keyLabel = QtWidgets.QLabel(self)
        self.keySequenceEdit.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.inputStrHLayout = QtWidgets.QHBoxLayout()
        self.inputStrLabel = QtWidgets.QLabel(self)
        self.inputStrLineEdit = QtWidgets.QLineEdit(self)
        self.mtimeHLayout = QtWidgets.QHBoxLayout()
        self.mtimeLabel = QtWidgets.QLabel(self)
        self.mtimeDoubleSpinBox = QtWidgets.QDoubleSpinBox(self)
        self.pathHLayout = QtWidgets.QHBoxLayout()
        self.pathLabel = QtWidgets.QLabel(self)
        self.pathLineEdit = QtWidgets.QLineEdit(self)
        self.pathBtn = QtWidgets.QPushButton(self)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)

        self.setupUi()

    def setupUi(self):
        self.setObjectName("ActionDialog")
        self.resize(510, 469)
        self.verticalLayout.setObjectName("verticalLayout")
        self.actionTypeHLayout.setObjectName("actionTypeHLayout")
        self.actionTypeLabel.setObjectName("actionTypeLabel")
        self.actionTypeHLayout.addWidget(self.actionTypeLabel)
        self.actionTypeComboBox.setObjectName("actionTypeComboBox")
        for k, v in auto_action.actionTypeName.items():
            self.actionTypeComboBox.addItem(v, k)
        self.actionTypeHLayout.addWidget(self.actionTypeComboBox)
        self.verticalLayout.addLayout(self.actionTypeHLayout)
        self.posHLayout.setObjectName("posHLayout")
        self.posLabel.setObjectName("posLabel")
        self.posHLayout.addWidget(self.posLabel)
        self.posLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.posLineEdit.setObjectName("posLineEdit")
        self.posHLayout.addWidget(self.posLineEdit)
        self.posBtn.setObjectName("posBtn")
        self.posHLayout.addWidget(self.posBtn)
        self.verticalLayout.addLayout(self.posHLayout)
        self.regionHLayout.setObjectName("regionHLayout")
        self.regionLabel.setObjectName("regionLabel")
        self.regionHLayout.addWidget(self.regionLabel)
        self.regionLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.regionLineEdit.setObjectName("regionLineEdit")
        self.regionHLayout.addWidget(self.regionLineEdit)
        self.regionBtn.setObjectName("regionBtn")
        self.regionHLayout.addWidget(self.regionBtn)
        self.verticalLayout.addLayout(self.regionHLayout)
        self.clickTypeHLayout.setObjectName("clickTypeHLayout")
        self.clickTypeLabel.setObjectName("clickTypeLabel")
        self.clickTypeHLayout.addWidget(self.clickTypeLabel)
        self.clickTypeComboBox.setObjectName("clickTypeComboBox")
        for k, v in auto_action.clickTypeName.items():
            self.clickTypeComboBox.addItem(v, k)
        self.clickTypeHLayout.addWidget(self.clickTypeComboBox)
        self.verticalLayout.addLayout(self.clickTypeHLayout)
        self.keyHLayout.setObjectName("keyHLayout")
        self.keyLabel.setObjectName("keyLabel")
        self.keyHLayout.addWidget(self.keyLabel)
        self.keySequenceEdit.setObjectName("keySequenceEdit")
        self.keyHLayout.addWidget(self.keySequenceEdit)
        self.verticalLayout.addLayout(self.keyHLayout)
        self.inputStrHLayout.setObjectName("inputStrHLayout")
        self.inputStrLabel.setObjectName("inputStrLabel")
        self.inputStrHLayout.addWidget(self.inputStrLabel)
        self.inputStrLineEdit.setObjectName("inputStrLineEdit")
        self.inputStrHLayout.addWidget(self.inputStrLineEdit)
        self.verticalLayout.addLayout(self.inputStrHLayout)
        self.mtimeHLayout.setObjectName("mtimeHLayout")
        self.mtimeLabel.setObjectName("mtimeLabel")
        self.mtimeHLayout.addWidget(self.mtimeLabel)
        self.mtimeDoubleSpinBox.setMaximum(10000.0)
        self.mtimeDoubleSpinBox.setObjectName("mtimeDoubleSpinBox")
        self.mtimeHLayout.addWidget(self.mtimeDoubleSpinBox)
        self.verticalLayout.addLayout(self.mtimeHLayout)
        self.pathHLayout.setObjectName("pathHLayout")
        self.pathLabel.setObjectName("pathLabel")
        self.pathHLayout.addWidget(self.pathLabel)
        self.pathLineEdit.setObjectName("pathLineEdit")
        self.pathHLayout.addWidget(self.pathLineEdit)
        self.pathBtn.setObjectName("pathBtn")
        self.pathHLayout.addWidget(self.pathBtn)
        self.verticalLayout.addLayout(self.pathHLayout)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)  # type: ignore
        self.buttonBox.rejected.connect(self.reject)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(self)

        self.actionTypeComboBox.setCurrentIndex(0)
        self.actionTypeComboBox.setCurrentIndex(1)
        self.actionTypeComboBox.setCurrentIndex(0)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("ActionDialog", "添加新动作"))
        self.actionTypeLabel.setText(_translate("ActionDialog", "选择动作类型"))
        self.posLabel.setText(_translate("ActionDialog", "坐标向量"))
        self.posLineEdit.setInputMask(_translate("ActionDialog", "(9999, 9999)"))
        self.posLineEdit.setText(_translate("ActionDialog", "(0000, 0000)"))
        self.posBtn.setText(_translate("ActionDialog", "选择坐标向量"))
        self.regionLabel.setText(_translate("ActionDialog", "选择区域"))
        self.regionLineEdit.setInputMask(_translate("ActionDialog", "(9999, 9999, 9999, 9999)"))
        self.regionLineEdit.setText(_translate("ActionDialog", "(0000, 0000, 1920, 1080)"))
        self.regionBtn.setText(_translate("ActionDialog", "选择区域"))
        self.clickTypeLabel.setText(_translate("ActionDialog", "选择点击类型"))
        self.keyLabel.setText(_translate("ActionDialog", "输入按键"))
        self.inputStrLabel.setText(_translate("ActionDialog", "文本输入"))
        self.mtimeLabel.setText(_translate("ActionDialog", "最大时间输入"))
        self.pathLabel.setText(_translate("ActionDialog", "图片路径输入"))
        self.pathBtn.setText(_translate("ActionDialog", "选择图片路径"))

    @pyqtSlot(int)
    def on_actionTypeComboBox_currentIndexChanged(self, __index: int):
        """
        根据 actionType 选中改变布局
        :param __index: 当前选中
        :return:
        """
        actionType = self.actionTypeComboBox.currentData()
        if actionType in [auto_action.MOUSE_MOVETO, auto_action.MOUSE_MOVEREL, auto_action.MOUSE_CLICK,
                          auto_action.MOUSE_DRAGTO, auto_action.MOUSE_DRAGREL]:
            self.posBtn.show()
            self.posLineEdit.show()
            self.posLabel.show()
        else:
            self.posBtn.hide()
            self.posLineEdit.hide()
            self.posLabel.hide()
        if actionType in [auto_action.KEYBOARD_COPY, auto_action.IMAGE_MOUSE_CLICK, auto_action.IMAGE_SCREENSHOT]:
            self.regionBtn.show()
            self.regionLabel.show()
            self.regionLineEdit.show()
        else:
            self.regionBtn.hide()
            self.regionLabel.hide()
            self.regionLineEdit.hide()
        if actionType in [auto_action.MOUSE_CLICK, auto_action.IMAGE_MOUSE_CLICK]:
            self.clickTypeComboBox.show()
            self.clickTypeLabel.show()
        else:
            self.clickTypeComboBox.hide()
            self.clickTypeLabel.hide()
        if actionType in [auto_action.KEYBOARD_KEY]:
            self.keyLabel.show()
            self.keySequenceEdit.show()
        else:
            self.keyLabel.hide()
            self.keySequenceEdit.hide()
        if actionType in [auto_action.COMMAND_RUN, auto_action.KEYBOARD_INPUT]:
            self.inputStrLabel.show()
            self.inputStrLineEdit.show()
        else:
            self.inputStrLabel.hide()
            self.inputStrLineEdit.hide()
        if actionType in [auto_action.TIME_DELAY, auto_action.ACTION_END, auto_action.IMAGE_WAIT]:
            self.mtimeLabel.show()
            self.mtimeDoubleSpinBox.show()
        else:
            self.mtimeLabel.hide()
            self.mtimeDoubleSpinBox.hide()
        if actionType in [auto_action.IMAGE_MOUSE_CLICK, auto_action.IMAGE_WAIT, auto_action.IMAGE_SCREENSHOT,
                          auto_action.IMAGE_MOVE]:
            self.pathBtn.show()
            self.pathLabel.show()
            self.pathLineEdit.show()
        else:
            self.pathBtn.hide()
            self.pathLabel.hide()
            self.pathLineEdit.hide()

    @pyqtSlot()
    def on_posBtn_clicked(self):
        self.showMinimized()
        x, y = utils.getPositionByKey()
        self.posLineEdit.setText("(%04d, %04d)" % (x, y))
        self.showNormal()

    @pyqtSlot()
    def on_regionBtn_clicked(self):
        self.showMinimized()
        left, top, width, height = utils.getBoxByKey()
        self.regionLineEdit.setText("(%04d, %04d, %04d, %04d)" % (left, top, width, height))
        self.showNormal()

    @pyqtSlot()
    def on_pathBtn_clicked(self):
        self.showMinimized()
        if not os.path.exists(utils.imagesPath):
            os.mkdir(utils.imagesPath)
        path = QtWidgets.QFileDialog.getOpenFileName(self, directory=utils.imagesPath, filter='*.png')
        if path is None:
            path = ''
        elif len(path) == 0:
            path = ''
        self.pathLineEdit.setText(path[0])
        self.showNormal()

    def getActionType(self):
        return self.actionTypeComboBox.currentData()

    def getPos(self) -> (int, int):
        cp = re.compile('^\((\d+), (\d+)\)')
        match = cp.match(self.posLineEdit.text())
        if len(match.groups()) < 2:
            return 0, 0
        x = int(match.group(1))
        y = int(match.group(2))
        pos = (x, y)
        return pos

    def getRegion(self) -> (int, int, int, int):
        cp = re.compile('^\((\d+), (\d+), (\d+), (\d+)\)')
        match = cp.match(self.regionLineEdit.text())
        if len(match.groups()) < 4:
            return 0, 0, 0, 0
        x = int(match.group(1))
        y = int(match.group(2))
        dx = int(match.group(3))
        dy = int(match.group(4))
        return x, y, dx, dy

    def getClickType(self) -> str:
        return self.clickTypeComboBox.currentData()

    def getKey(self) -> list:
        return self.keySequenceEdit.keySequence().toString().split('+')

    def getInputStr(self) -> str:
        return self.inputStrLineEdit.text()

    def getMtime(self) -> float:
        return self.mtimeDoubleSpinBox.value()

    def getPath(self) -> str:
        return self.pathLineEdit.text().strip()


    def getImgStr(self):
        return utils.imgToStr(PIL.Image.open(self.getPath()))

    def getAction(self) -> dict:
        """
        获取输入数据
        :return: 输入数据
        """
        data = {'actionType': self.getActionType()}
        if not self.posLineEdit.isHidden():
            data['pos'] = self.getPos()
        if not self.regionLineEdit.isHidden():
            data['region'] = self.getRegion()
        if not self.clickTypeComboBox.isHidden():
            data['clickType'] = self.getClickType()
        if not self.keySequenceEdit.isHidden():
            data['key'] = self.getKey()
        if not self.inputStrLineEdit.isHidden():
            data['inputStr'] = self.getInputStr()
        if not self.mtimeDoubleSpinBox.isHidden():
            data['mtime'] = self.getMtime()
        if not self.pathLineEdit.isHidden():
            if self.getActionType() == auto_action.IMAGE_SCREENSHOT:
                data['path'] = self.getPath()
            else:
                data['imgStr'] = self.getImgStr()
        return data


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, actionGroupDict: None | dict[str, auto_action.ActionGroup] = None):
        super(MainWindow, self).__init__(parent)
        self.TAG = "MainWindow[]"
        # ui 变量
        self.centralWidget = QtWidgets.QWidget(self)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.actionGroupListView = QtWidgets.QListView(self.centralWidget)
        self.actionVLayout = QtWidgets.QVBoxLayout()
        self.actionHLayout = QtWidgets.QHBoxLayout()
        self.addActionBtn = QtWidgets.QPushButton(self.centralWidget)
        self.delActionBtn = QtWidgets.QPushButton(self.centralWidget)
        self.runActionBtn = QtWidgets.QPushButton(self.centralWidget)
        self.upActionBtn = QtWidgets.QPushButton(self.centralWidget)
        self.downActionBtn = QtWidgets.QPushButton(self.centralWidget)
        self.actionListView = QtWidgets.QListView(self.centralWidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.aboutAction = QtWidgets.QAction(self)
        self.addActionGroupAction = QtWidgets.QAction(self)
        self.screenShotAction = QtWidgets.QAction(self)
        self.authorWidget = AuthorWidget()
        self.authorWidget.hide()

        self.addActionGroupAction = QtWidgets.QAction(self)
        self.delActionGroupAction = QtWidgets.QAction(self)
        self.copyActionGroupAction = QtWidgets.QAction(self)
        self.importActionGroupAction = QtWidgets.QAction(self)

        # 数据变量
        if actionGroupDict is None:
            actionGroupDict = {}
        self.actionGroupDict = actionGroupDict
        self.isRunning = False

        self.actionGroupListModel = QtCore.QStringListModel()
        self.actionGroupListModel.setStringList(self.actionGroupDict.keys())
        self.actionGroupListView.setModel(self.actionGroupListModel)

        self.actionListModel = QtCore.QStringListModel()
        self.actionListModel.setStringList([])
        self.actionListView.setModel(self.actionListModel)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(800, 600)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.actionGroupListView.setObjectName("actionGroupListView")
        self.horizontalLayout.addWidget(self.actionGroupListView)
        self.actionVLayout.setObjectName("actionVLayout")
        self.actionHLayout.setObjectName("actionHLayout")
        self.addActionBtn.setObjectName("addActionBtn")
        self.actionHLayout.addWidget(self.addActionBtn)
        self.delActionBtn.setObjectName("delActionBtn")
        self.actionHLayout.addWidget(self.delActionBtn)
        self.runActionBtn.setObjectName("runActionBtn")
        self.actionHLayout.addWidget(self.runActionBtn)
        self.upActionBtn.setObjectName("upActionBtn")
        self.actionHLayout.addWidget(self.upActionBtn)
        self.downActionBtn.setObjectName("downActionBtn")
        self.actionHLayout.addWidget(self.downActionBtn)
        self.actionVLayout.addLayout(self.actionHLayout)
        self.actionListView.setObjectName("actionListView")
        self.actionVLayout.addWidget(self.actionListView)
        self.horizontalLayout.addLayout(self.actionVLayout)
        self.setCentralWidget(self.centralWidget)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.aboutAction.setObjectName("aboutAction")
        self.menubar.addAction(self.aboutAction)
        self.screenShotAction.setObjectName("screenShotAction")
        self.menubar.addAction(self.screenShotAction)
        self.addActionGroupAction.setObjectName("addActionGroupAction")
        self.delActionGroupAction.setObjectName("delActionGroupAction")
        self.copyActionGroupAction.setObjectName("copyActionGroupAction")
        self.importActionGroupAction.setObjectName("importActionGroupAction")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.actionGroupListView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.actionGroupListView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.actionGroupListView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.actionListView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.actionListView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.addActionBtn.setText(_translate("MainWindow", "添加新动作"))
        self.delActionBtn.setText(_translate("MainWindow", "移除选中动作"))
        self.runActionBtn.setText(_translate("MainWindow", "运行选中动作组"))
        self.upActionBtn.setText(_translate("MainWindow", "上移"))
        self.downActionBtn.setText(_translate("MainWindow", "下移"))
        self.aboutAction.setText(_translate("MainWindow", "关于"))
        self.screenShotAction.setText(_translate("MainWindow", "截图"))
        self.addActionGroupAction.setText(_translate("MainWindow", "添加新动作组"))
        self.delActionGroupAction.setText(_translate("MainWindow", "删除选中动作组"))
        self.copyActionGroupAction.setText(_translate("MainWindow", "复制到剪贴板"))
        self.importActionGroupAction.setText(_translate("MainWindow", "从剪贴板导入"))

    @pyqtSlot()
    def on_aboutAction_triggered(self):
        """
        信息界面
        :return:
        """
        self.authorWidget.show()

    @pyqtSlot()
    def on_screenShotAction_triggered(self):
        """
        截图
        :return:
        """
        self.hide()
        utils.screenShotByKey()
        self.show()

    @pyqtSlot(QPoint)
    def on_actionGroupListView_customContextMenuRequested(self, pos):
        """
        打开动作组窗口
        :param pos: 鼠标当前位置
        :return:
        """
        menu = QtWidgets.QMenu()
        menu.addAction(self.addActionGroupAction)
        menu.addAction(self.delActionGroupAction)
        menu.addAction(self.copyActionGroupAction)
        menu.addAction(self.importActionGroupAction)
        menu.exec_(self.actionGroupListView.mapToGlobal(pos))

    @pyqtSlot()
    def on_addActionGroupAction_triggered(self):
        dialog = ActionGroupNameDialog()
        self.hide()
        dialog.show()
        res = dialog.exec()
        if res == QtWidgets.QDialog.Accepted:
            name = dialog.getInput()
            self.addNewActionGroup(name=name)
        self.show()

    @pyqtSlot()
    def on_delActionGroupAction_triggered(self):
        name = self.getSelectedActionGroupName()
        if name is None:
            return
        self.delActionGroup(name)

    @pyqtSlot()
    def on_copyActionGroupAction_triggered(self):
        name = self.getSelectedActionGroupName()
        if name is None:
            return
        pyperclip.copy(self.actionGroupDict[name].json())

    @pyqtSlot()
    def on_importActionGroupAction_triggered(self):
        dialog = ActionGroupNameDialog()
        self.hide()
        dialog.show()
        res = dialog.exec()
        if res == QtWidgets.QDialog.Accepted:
            name = dialog.getInput()
            dataList = json.loads(pyperclip.paste())
            print(dataList)
            self.addNewActionGroup(name, dataList)
        self.show()

    @pyqtSlot(QModelIndex)
    def on_actionGroupListView_clicked(self):
        """
        刷新 actionListView
        :return:
        """
        self.upgradeActionListView()

    @pyqtSlot()
    def on_addActionBtn_clicked(self):
        """
        添加新动作
        :return:
        """
        if self.getSelectedActionGroupName() is None:
            return
        dialog = ActionDialog()
        self.hide()
        dialog.show()
        res = dialog.exec()
        if res == QtWidgets.QDialog.Accepted:
            action = dialog.getAction()
            self.addNewAction(action)
        self.show()

    @pyqtSlot()
    def on_delActionBtn_clicked(self):
        """
        删除选中动作
        :return:
        """
        index = self.getSelectedActionRow()
        if index == -1:
            return
        self.delAction(index)

    @pyqtSlot()
    def on_runActionBtn_clicked(self):
        """
        运行动作组
        :return:
        """
        name = self.getSelectedActionGroupName()
        if name is None:
            return
        self.showMinimized()
        self.runActionBtn.setEnabled(False)
        self.runSelectedActionGroup(self.getSelectedActionGroupName())
        self.runActionBtn.setEnabled(True)
        self.showNormal()

    @pyqtSlot()
    def on_upActionBtn_clicked(self):
        """
        上移选中动作
        :return:
        """
        row = self.getSelectedActionRow()
        if row == 0 or row == -1:
            return
        else:
            self.swapAction(row, row - 1)
            self.actionListView.setCurrentIndex(self.actionListModel.index(row - 1))

    @pyqtSlot()
    def on_downActionBtn_clicked(self):
        """
        下移选中动作
        :return:
        """
        row = self.getSelectedActionRow()
        if row >= self.actionListModel.rowCount() - 1 or row <= -1:
            return
        else:
            self.swapAction(row, row + 1)
            self.actionListView.setCurrentIndex(self.actionListModel.index(row + 1))

    def getSelectedActionGroupName(self) -> None | str:
        """
        获取选中的动作组
        :return: 选中的动作组的 name
        """
        if len(self.actionGroupListView.selectedIndexes()) > 0:
            index = self.actionGroupListView.selectedIndexes()[0]
            return index.data()
        else:
            return None

    def getSelectedActionRow(self):
        """
        获取选中的动作的下标，默认为 -1
        :return: 选中的动作的下标，若无，则返回 -1
        """
        if len(self.actionListView.selectedIndexes()) > 0:
            index = self.actionListView.selectedIndexes()[0]
            return index.row()
        else:
            return - 1

    def upgradeActionListView(self):
        """
        更新 actionListView 内容
        :return:
        """
        name = self.getSelectedActionGroupName()
        if name is None:
            self.actionListModel.setStringList([])
        else:
            actionGroup = self.actionGroupDict[name]
            self.actionListModel.setStringList(actionGroup.explainList)

    def addNewActionGroup(self, name: str, dataList=None):
        """
        添加动作组
        :param name: 新动作组名字
        :param dataList: 新动作组数据
        :return:
        """
        if dataList is None:
            dataList = []
        if name in self.actionGroupDict.keys():
            i = 0
            while name + f"({i})" in self.actionGroupDict.keys():
                i += 1
            name = name + f"({i})"
        row = self.actionGroupListModel.rowCount()
        try:
            # 数据部分
            actonGroup = auto_action.ActionGroup(name=name, dataList=dataList)
            self.actionGroupDict[name] = actonGroup
            self.actionGroupDict[name].save()

            # ui 部分
            self.actionGroupListModel.insertRow(row)
            self.actionGroupListModel.setData(self.actionGroupListModel.index(row), name)
        except KeyError:
            return

    def delActionGroup(self, name: str | None):
        """
        删除名称为 name 的动作组
        :param name 动作组名称
        :return:
        """
        if name is None:
            return
        index = self.actionGroupListView.selectedIndexes()[0]
        # 数据部分
        self.actionGroupDict[name].deleteFile()
        self.actionGroupDict.pop(name)

        # ui 部分
        self.actionGroupListView.clearSelection()
        self.actionGroupListModel.removeRow(index.row())
        self.actionListModel.setStringList([])

    def addNewAction(self, data: dict):
        """
        在末尾添加新动作
        :param data: 动作data
        :return:
        """
        name = self.getSelectedActionGroupName()
        if name is None:
            return
        row = self.actionListModel.rowCount()

        # 数据部分
        self.actionGroupDict[name].insert(row, data)
        self.actionGroupDict[name].save()

        # ui 部分
        self.upgradeActionListView()

    def delAction(self, index: int):
        """
        删除动作
        :param index 需要删除的动作的下标
        :return:
        """
        name = self.getSelectedActionGroupName()
        if name is None:
            return

        # 数据部分
        self.actionGroupDict[name].pop(index)
        self.actionGroupDict[name].save()

        # ui 部分
        self.upgradeActionListView()

    def swapAction(self, index1: int, index2: int):
        """
        交换 index1, index2 处动作
        :param index1: 下标1
        :param index2: 下表2
        :return:
        """
        name = self.getSelectedActionGroupName()
        if name is None:
            return

        # 数据部分
        self.actionGroupDict[name].swap(index1, index2)
        self.actionGroupDict[name].save()

        # ui 部分
        self.upgradeActionListView()

    def runSelectedActionGroup(self, name: str | None):
        """
        运行选中动作组
        :param name 动作组名称
        :return:
        """
        if name is None:
            return
        else:
            self.actionGroupDict[name].run()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        logger.debug(self.TAG + ": is closed.")
        # 关闭窗口后，自动保存（占用线程，暂时不用）
        # for name, actionGroup in self.actionGroupDict.items():
        #     actionGroup.save()
