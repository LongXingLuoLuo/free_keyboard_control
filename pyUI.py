# -*- coding:UTF-8 -*-

from PyQt5 import QtWidgets, QtCore, QtGui

import auto_action


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, actionGroupDict: None | dict[str, auto_action.ActionGroup] = None):
        super(MainWindow, self).__init__(parent)
        # ui 变量
        self.centralWidget = QtWidgets.QWidget(self)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.actionGroupListView = QtWidgets.QListView(self.centralWidget)
        self.actionVLayout = QtWidgets.QVBoxLayout()
        self.actionHLayout = QtWidgets.QHBoxLayout()
        self.addActionBtn = QtWidgets.QPushButton(self.centralWidget)
        self.removeActionBtn = QtWidgets.QPushButton(self.centralWidget)
        self.flushActionBtn = QtWidgets.QPushButton(self.centralWidget)
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
        self.removeActionBtn.setObjectName("removeActionBtn")
        self.actionHLayout.addWidget(self.removeActionBtn)
        self.flushActionBtn.setObjectName("flushActionBtn")
        self.actionHLayout.addWidget(self.flushActionBtn)
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
        self.actionGroupListView.customContextMenuRequested.connect(self.showActionGroupMenu)
        self.actionGroupListView.clicked.connect(self.on_actionGroupListView_click)

        self.actionListView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.actionListView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.actionListView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.actionListView.customContextMenuRequested.connect(self.showActionMenu)


    def getSelectedActionGroupName(self) -> None | str:
        if len(self.actionGroupListView.selectedIndexes()) > 0:
            index = self.actionGroupListView.selectedIndexes()[0]
            return index.data()
        else:
            return None

    def on_actionGroupListView_click(self, index: QtCore.QModelIndex):
        self.upgradeActeeionListView()

    def upgradeActeeionListView(self):
        name = self.getSelectedActionGroupName()
        if name is None:
            self.actionListModel.setStringList([])
        else:
            actionGroup = self.actionGroupDict[name]
            self.actionListModel.setStringList(actionGroup.typeList())

    def showActionGroupMenu(self, pos):
        # index = self.actionGroupListView.indexAt(pos)
        menu = QtWidgets.QMenu()
        addAction = menu.addAction("插入新动作组")
        delAction = menu.addAction("删除选中动作组")
        action = menu.exec_(self.actionGroupListView.mapToGlobal(pos))
        if action == addAction:
            self.addNewActionGroup()
        elif action == delAction:
            self.delSelectedActionGroup()

    def showActionMenu(self, pos):
        index = self.actionGroupListView.indexAt(pos)
        menu = QtWidgets.QMenu()
        addAction = menu.addAction("插入新动作")
        delAction = menu.addAction("删除选中动作")
        action = menu.exec_(self.actionGroupListView.mapToGlobal(pos))
        if action == addAction:
            self.addNewAction(index)
        elif action == delAction:
            self.delSelectedAction(index)

    def addNewActionGroup(self):
        """
        添加动作组
        :return:
        """
        name = 'three'
        actonGroup = auto_action.ActionGroup()
        actonGroup.append(auto_action.generateAction(actionType=auto_action.ACTION_END))

        # 添加
        row = self.actionGroupListModel.rowCount()
        if len(self.actionGroupListView.selectedIndexes()) > 0:
            row = self.actionGroupListView.selectedIndexes()[0].row() + 1
        i = 1
        while name + f"({i})" in self.actionGroupDict.keys():
            i += 1
        name = name + f"({i})"
        # ui 部分
        self.actionGroupListModel.insertRow(row)
        self.actionGroupListModel.setData(self.actionGroupListModel.index(row), name)

        # 数据部分
        self.actionGroupDict[name] = actonGroup
        actonGroup.save(name)

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
        self.actionGroupDict.pop(name)
        auto_action.delJson(name)

    def addNewAction(self, __index):
        name = self.getSelectedActionGroupName()
        action = auto_action.generateAction(actionType=auto_action.TIME_DELAY, mtime=1000)
        row = __index.row() + 1
        if name is None:
            return
        # 数据部分
        self.actionGroupDict[name].insert(row, action)
        self.actionGroupDict[name].save(name)
        # ui 部分
        self.upgradeActeeionListView()


    def delSelectedAction(self, __index):
        name = self.getSelectedActionGroupName()
        row = __index.row() + 1
        if name is None:
            return
        # 数据部分
        self.actionGroupDict[name].pop(row)
        self.actionGroupDict[name].save(name)
        # ui 部分
        self.upgradeActeeionListView()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.addActionBtn.setText(_translate("MainWindow", "添加动作"))
        self.removeActionBtn.setText(_translate("MainWindow", "移除动作"))
        self.flushActionBtn.setText(_translate("MainWindow", "刷新动作"))
        self.aboutMenu.setTitle(_translate("MainWindow", "about"))
        self.authorAction.setText(_translate("MainWindow", "作者介绍"))

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        for name, actionGroup in self.actionGroupDict.items():
            actionGroup.save(name)
