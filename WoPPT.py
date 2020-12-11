# -*- coding: utf-8 -*-
import sys, os
os.chdir(os.path.dirname(os.path.abspath("__file__")))
from mainWin import mainWin
from PyQt5 import QtCore, QtGui, QtWidgets
from AddStep import addStep
from RunThread import runThread
from LogUI import logUI


class logicPart(mainWin):
    def __init__(self):
        super(logicPart, self).__init__()
        self.funcPart()

    def funcPart(self):
        self.pipelineInitial()
        self.log = logUI()

        self.listWidget_2.currentItemChanged.connect(self.changeBetweenItem)
        self.listWidget_2.itemDoubleClicked.connect(self.doubleClicked)
        self.listWidget_2.itemChanged.connect(self.itemChange)

    # initial pipeline GUI
    def pipelineInitial(self):
        # initial class name
        global classCount
        classCount = 2
        self.lineCount = 1

        # set a global dict for handling different pipeline
        self.pipelineDict = {}

        self.listWidget_2.addItem("Pipeline")
        self.listWidget_2.setCurrentRow(0)
        self.nowItem = self.listWidget_2.currentItem()
        self.nowItem.setFlags(self.nowItem.flags() | QtCore.Qt.ItemIsEditable)
        self.listWidget_2.addItem("Pipeline1")
        self.listWidget_2.setCurrentRow(1)
        self.nowItem = self.listWidget_2.currentItem()
        self.nowItem.setFlags(self.nowItem.flags() | QtCore.Qt.ItemIsEditable)
        self.listWidget_2.setCurrentRow(0)

        # add first item
        self.item = QtWidgets.QListWidgetItem()
        self.item.setSizeHint(QtCore.QSize(100, 40))
        self.listWidget.addItem(self.item)

        self.oneStep0 = addStep()
        self.oneStep0.setObjectName("oneStep0")
        self.listWidget.setItemWidget(self.item, self.oneStep0)

    @QtCore.pyqtSlot(QtWidgets.QListWidgetItem, QtWidgets.QListWidgetItem)
    def changeBetweenItem(self, current, previous):
        print("changeBetweenItem called")
        # save data
        self.getInput()
        try:
            print("previous", previous.text())
            if self.execCode != []:
                self.pipelineDict[previous.text()] = self.execCode
        except Exception as e:
            print("err", e)
        self.listWidget.takeItem(0)
        self.listWidget.clear()
        self.lineCount = 0
        self.addOneStep()
        print("change between item pipelineDict", self.pipelineDict)
        # set pipeline text
        try:
            self.pipelineSetText(current.text())
        except AttributeError:
            pass

    @QtCore.pyqtSlot(QtWidgets.QListWidgetItem)
    def itemChange(self, item):
        print("itemChange called")
        # update dict
        # signal emit when add new item
        print("Item change", item.text())
        new = item.text()
        try:
            if new != self.changeName and self.changeName in self.pipelineDict.keys():
                self.pipelineDict[new] = self.pipelineDict[self.changeName]
                del self.pipelineDict[self.changeName]
        except AttributeError:
            pass
        print("Dict", self.pipelineDict)

    @QtCore.pyqtSlot(QtWidgets.QListWidgetItem)
    def doubleClicked(self, item):
        print("doubleClicked called")
        self.changeName = item.text()
        print("changeName", self.changeName)

    def pipelineSetText(self, ID):
        if ID in self.pipelineDict.keys():
            n = len(self.pipelineDict[ID])
            textList = self.pipelineDict[ID]
            self.lineCount = 1
            for i in range(n):
                # except initial step
                if i != n - 1:
                    self.addOneStep()
                className = eval("self.oneStep" + str(i))

                # set each line text
                print(textList)
                if textList[i] != []:
                    className.lineEditsw.setText(textList[i][0])
                    className.lineEditpm.setText(textList[i][1])
                    className.inputFile.setText(textList[i][2])
                    className.lineEditsc.setText(textList[i][3])
                    className.outputFile.setText(textList[i][4])
            self.lineCount = 1

    def showLog(self):
        self.log.show()

    def runningThread(self):
        self.getInput()
        self.workThread = runThread(self.execStr)
        self.workThread.start()
        self.statusBar().showMessage("Running")
        self.workThread.trigger.connect(self.finishThread)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    logic = logicPart()
    logic.show()
    sys.exit(app.exec_())
