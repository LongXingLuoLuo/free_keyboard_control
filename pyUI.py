# -*- coding:UTF-8 -*-

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot, QPoint, QModelIndex

import auto_action
from log_config import logger


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

        # 数据变量
        if actionGroupDict is None:
            actionGroupDict = {}
        self.actionGroupDict = actionGroupDict

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
        self.hide()
        self.runSelectedActionGroup()
        self.show()


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
        self.addActionBtn.setText(_translate("MainWindow", "添加动作"))
        self.delActionBtn.setText(_translate("MainWindow", "移除动作"))
        self.runActionBtn.setText(_translate("MainWindow", "运行动作组"))
        self.aboutMenu.setTitle(_translate("MainWindow", "关于"))
        self.authorAction.setText(_translate("MainWindow", "作者介绍"))

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        logger.debug(self.TAG + ": is closed.")
        for name, actionGroup in self.actionGroupDict.items():
            actionGroup.save()
