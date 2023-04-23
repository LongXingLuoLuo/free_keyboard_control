# -*- coding:UTF-8 -*-
from threading import Thread

import pynput.keyboard
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot, QPoint, QModelIndex

import auto_action
from log_config import logger


class AuthorWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AuthorWidget, self).__init__(parent)
        self.verticalLayout = None
        self.textBrowser = None
        self.setupUi()

    def setupUi(self):
        self.setObjectName("authorWidget")
        self.resize(534, 419)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowser = QtWidgets.QTextBrowser(self)
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
                                            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"> </p></body></html>"))


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
        self.actionListView = QtWidgets.QListView(self.centralWidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.aboutMenu = QtWidgets.QMenu(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.authorAction = QtWidgets.QAction(self)
        self.addActionGroupAction = QtWidgets.QAction(self)
        self.authorWidget = AuthorWidget()
        self.authorWidget.hide()

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
        self.actionVLayout.addLayout(self.actionHLayout)
        self.actionListView.setObjectName("actionListView")
        self.actionVLayout.addWidget(self.actionListView)
        self.horizontalLayout.addLayout(self.actionVLayout)
        self.setCentralWidget(self.centralWidget)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.aboutMenu.setObjectName("aboutMenu")
        self.setMenuBar(self.menubar)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.authorAction.setObjectName("authorAction")
        self.aboutMenu.addAction(self.authorAction)
        self.menubar.addAction(self.aboutMenu.menuAction())

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.actionGroupListView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.actionGroupListView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.actionGroupListView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.actionListView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.actionListView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.actionListView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

    @pyqtSlot()
    def on_authorAction_triggered(self):
        self.authorWidget.show()


    @pyqtSlot(QPoint)
    def on_actionGroupListView_customContextMenuRequested(self, pos):
        """
        打开动作组窗口
        :param pos:
        :return:
        """
        menu = QtWidgets.QMenu()
        addAction = menu.addAction("插入新动作组")
        delAction = menu.addAction("删除选中动作组")
        action = menu.exec_(self.actionGroupListView.mapToGlobal(pos))
        if action == addAction:
            self.addNewActionGroup()
        elif action == delAction:
            self.delSelectedActionGroup()

    @pyqtSlot(QModelIndex)
    def on_actionGroupListView_clicked(self):
        """
        actionGroupListView 点击事件, 刷新 actionListView
        :return:
        """
        self.upgradeActionListView()

    @pyqtSlot()
    def on_addActionBtn_clicked(self):
        # self.addNewAction()
        self.addNewAction()

    @pyqtSlot()
    def on_delActionBtn_clicked(self):
        self.delSelectedAction()

    @pyqtSlot()
    def on_runActionBtn_clicked(self):
        name = self.getSelectedActionGroupName()
        if name is None:
            return
        self.showMinimized()
        self.runActionBtn.setEnabled(False)
        self.runSelectedActionGroup()
        self.runActionBtn.setEnabled(True)
        self.showNormal()

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
            return -1

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
            self.actionListModel.setStringList(actionGroup.typeList())

    def addNewActionGroup(self):
        """
        添加动作组
        :return:
        """
        name = 'three'
        i = 1
        row = self.actionGroupListModel.rowCount()
        while name + f"({i})" in self.actionGroupDict.keys():
            i += 1
        name = name + f"({i})"
        actonGroup = auto_action.ActionGroup(name=name)
        self.actionGroupDict[name] = actonGroup

        # 数据部分
        self.actionGroupDict[name].save()

        # ui 部分
        self.actionGroupListModel.insertRow(row)
        self.actionGroupListModel.setData(self.actionGroupListModel.index(row), name)

    def delSelectedActionGroup(self):
        """
        删除选中行
        :return:
        """
        if len(self.actionGroupListView.selectedIndexes()) == 0:
            return
        index = self.actionGroupListView.selectedIndexes()[0]
        name = index.data()

        # ui 部分
        self.actionGroupListView.clearSelection()
        self.actionGroupListModel.removeRow(index.row())
        self.actionListModel.setStringList([])

        # 数据部分
        self.actionGroupDict[name].deleteFile()
        self.actionGroupDict.pop(name)

    def addNewAction(self):
        name = self.getSelectedActionGroupName()
        if name is None:
            return
        action = auto_action.generateAction(actionType=auto_action.TIME_DELAY, mtime=1000)
        row = self.getSelectedActionRow() + 1

        # 数据部分
        self.actionGroupDict[name].insert(row, action)
        self.actionGroupDict[name].save()

        # ui 部分
        self.upgradeActionListView()

    def delSelectedAction(self):
        name = self.getSelectedActionGroupName()
        if name is None:
            return
        row = self.getSelectedActionRow()
        if row == -1:
            return
        # 数据部分
        self.actionGroupDict[name].pop(row)
        self.actionGroupDict[name].save()

        # ui 部分
        self.upgradeActionListView()

    def runSelectedActionGroup(self):
        """
        运行选中动作组
        :return:
        """
        name = self.getSelectedActionGroupName()
        if name is None:
            return
        else:
            self.actionGroupDict[name].run()


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.addActionBtn.setText(_translate("MainWindow", "插入动作"))
        self.delActionBtn.setText(_translate("MainWindow", "移除动作"))
        self.runActionBtn.setText(_translate("MainWindow", "运行动作组"))
        self.aboutMenu.setTitle(_translate("MainWindow", "关于"))
        self.authorAction.setText(_translate("MainWindow", "作者介绍"))

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        logger.debug(self.TAG + ": is closed.")
        for name, actionGroup in self.actionGroupDict.items():
            actionGroup.save()
