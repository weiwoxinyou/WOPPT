# -*- coding: utf-8 -*-

import os
os.chdir(os.path.dirname(os.path.abspath("__file__")))
from PyQt5 import QtCore, QtGui, QtWidgets
from Layout import Ui_MainWindow
from AddStep import addStep
import json

class mainWin(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mainWin, self).__init__()
        self.save = False
        self.setupUi(self)
        self.initUI()
    
    def initUI(self):

        self.bindToKey()
        self.basicLayout()
        self.shortcutLayout()
        self.adddelPipeline()
        self.center()

        '''
        self.verticalLayout_2.addWidget(self.frame, 0, QtCore.Qt.AlignTop)
        
        self.widgetFrame.setMaximumSize(QtCore.QSize(16777215, 43))
        self.l.itemSelectionChanged.connect()
        '''

    # add and del one pipeline
    def adddelPipeline(self):
        global classCount
        classCount = 2
        self.addPipelineButton.clicked.connect(self.newPipeline)
        self.delPipelineButton.clicked.connect(self.delPipeline)

    def newPipeline(self):
        self.getInput()
        temp = self.listWidget_2.currentItem().text()
        print("temp", temp)
        print("execCode, temp", self.execCode)
        self.pipelineDict[temp] = self.execCode if self.execCode != [] else []
        print("temp dict:", self.pipelineDict)
        # initial item
        self.listWidget.takeItem(0)
        self.listWidget.clear()
        global classCount
        self.lineCount = 0
        self.addOneStep()
        self.listWidget_2.addItem(f"Pipeline{classCount}")
        try:
            self.item = self.listWidget_2.item(classCount)
            self.item.setFlags(self.item.flags() | QtCore.Qt.ItemIsEditable)
        except AttributeError:
            pass
        self.listWidget_2.setCurrentRow(self.listWidget_2.count() - 1)
        self.nowItem = self.listWidget_2.currentItem()
        self.nowItem.setFlags(self.nowItem.flags() | QtCore.Qt.ItemIsEditable)

        classCount += 1

    def delPipeline(self):
        for SelectedItem in self.listWidget_2.selectedItems():
            self.listWidget_2.takeItem(self.listWidget_2.row(SelectedItem))

    def bindToKey(self):
        # bind to function
        self.Run.clicked.connect(self.runningThread)
        self.Add.clicked.connect(self.addOneStep)
        self.Del.clicked.connect(self.delStep)
        self.Log.clicked.connect(self.showLog)
        self.Shell.clicked.connect(self.outShell)
    
    def basicLayout(self):
        
        # layout
        self.verticalLayout_2.setContentsMargins(5, 0, 9, 0)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)

        # splitter control
        # 0: add del; 01: 0, pipeline; 1: button, software; 2: 01, 1
        # add & del button
        self.sideFrame = QtWidgets.QFrame()
        self.sideLayout = QtWidgets.QHBoxLayout(self.sideFrame)
        self.sideFrame.resize(40, 20)
        self.addPipelineButton = QtWidgets.QPushButton()
        self.delPipelineButton = QtWidgets.QPushButton()
        self.addIcon = QtGui.QIcon("./icon/add.svg")
        self.delIcon = QtGui.QIcon("./icon/del.svg")
        self.addPipelineButton.setIcon(self.addIcon)
        self.delPipelineButton.setIcon(self.delIcon)
        self.addPipelineButton.setIconSize(QtCore.QSize(30, 30))
        self.delPipelineButton.setIconSize(QtCore.QSize(30, 30))
        self.addPipelineButton.setMaximumSize(30, 30)
        self.delPipelineButton.setMaximumSize(30, 30)

        self.sideLayout.addWidget(self.addPipelineButton)
        self.sideLayout.addWidget(self.delPipelineButton)
        self.sideLayout.addStretch(2)

        # insert left pipeline widget
        self.splitter01 = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.splitter01.addWidget(self.sideFrame)
        self.splitter01.addWidget(self.listWidget_2)

        # insert right frame
        self.splitter1 = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.splitter1.addWidget(self.widgetFrame)
        self.splitter1.addWidget(self.frame)
        self.splitter1.addWidget(self.listWidget)

        self.splitter2 = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.splitter2.addWidget(self.splitter01) # left list
        self.splitter2.addWidget(self.splitter1) # right list
        self.splitter2.setSizes([40,500])

        self.verticalLayout_2.addWidget(self.splitter2)

        self.widgetFrame.resize(300, 20)


        # set button tooltop
        self.Run.setToolTip("Run the pipeline on this computer")
        self.Add.setToolTip("Add one item to this pipeline")
        self.Del.setToolTip("Delete selected item from this pipeline")
        self.Log.setToolTip("Check the log of this pipeline")
        self.Shell.setToolTip("Output a file of this pipeline for shell command")
        self.addPipelineButton.setToolTip("Create a new pipeline")
        self.delPipelineButton.setToolTip("Delete a pipeline")

    def shortcutLayout(self):
        self.actionNew.setShortcut("Ctrl+N")
        self.actionNew.setStatusTip("Drop all contents and create a new file")
        self.actionLoad.setShortcut("Ctrl+L")
        self.actionLoad.setStatusTip("Load a pipeline file")
        self.actionSave.setShortcut("Ctrl+S")
        self.actionSave.setStatusTip("Save a pipeline file")
        self.actionSave_as.setStatusTip("Save as any type file")

        self.actionNew.triggered.connect(self.newFile)
        self.actionLoad.triggered.connect(self.loadFile)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionSave_as.triggered.connect(self.saveFileAs)

    def getInput(self):
        # create pipeline
        self.execCode = []
        for i in range(self.listWidget.count()):
            try:
                className = eval("self.oneStep" + str(i))
                print("i", i)
                # get the input text
                swname = className.lineEditsw.text()
                pmname = className.lineEditpm.text()
                inname = className.inputFile.text()
                scname = className.lineEditsc.text()
                outname = className.outputFile.text()
                # software parameter infile script outfile
                if swname != "" or inname != "":
                    self.execCode.append([swname, pmname, inname, scname, outname])
                else:
                    pass # ignore all empty item
            except RuntimeError:
                pass # ignore remove item
        
        self.execStr = "\n".join(" ".join(x) for x in self.execCode)
        print("execCode:", self.execCode)
        
    def outShell(self):
        
        # change the input str to shell code
        
        self.getInput()
        self.shellStr = ""
        for i in self.execCode:
            line = " ".join(i)
            self.shellStr += f"nohup {line} &\n"
            
        outname, status = QtWidgets.QFileDialog.getSaveFileName(self, \
            "Save", '', "All Files (*);;Pipeline Files (*.pipeline)", \
            "Pipeline Files (*.pipeline)")
        with open(outname, 'w') as f:
            f.write(self.shellStr)

    def finishThread(self, fStr): 
        self.log.textB.setText(fStr)
        self.statusBar().showMessage("Finished")
        
    def addOneStep(self):
        print("add one step called, linecount = ", self.lineCount)
        n = self.lineCount
        print("lineCount:", self.lineCount)
        self.__dict__[f'oneStep{n}'] = addStep()
        self.__dict__[f'oneStep{n}'].setObjectName("oneStep" + str(n))

        self.item = QtWidgets.QListWidgetItem()
        self.item.setSizeHint(QtCore.QSize(100, 40))
        self.listWidget.addItem(self.item)
        self.listWidget.setItemWidget(self.item, self.__dict__[f'oneStep{n}'])

        self.lineCount += 1

        print("add one step finished, linecount = ", self.lineCount)

    def delStep(self):
        
        if not self.listWidget.selectedItems():
            QtWidgets.QMessageBox.information(self, "Tips", \
                "Please choose one item !", QtWidgets.QMessageBox.Ok)
            return
        self.lineCount -= 1
        for SelectedItem in self.listWidget.selectedItems():
            self.listWidget.takeItem(self.listWidget.row(SelectedItem))

    def center(self):
        frameGeometry = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        frameGeometry.moveCenter(centerPoint)
        self.move(frameGeometry.topLeft())

    def newFile(self):
        self.listWidget_2.clear()
        self.listWidget.takeItem(0)
        self.listWidget.clear()
        self.pipelineInitial()
        self.listWidget_2.setCurrentRow(1)
        self.listWidget_2.setCurrentRow(0)

    def loadFile(self):
        try:
            self.filename, status = QtWidgets.QFileDialog.getOpenFileName(self,
                            "Load File", "","All Files (*);;Log Files (*.log)", "Log Files (*.log)")
            with open(self.filename, 'r') as f:
                self.pipelineDict = json.load(f)
            firstPipeline = list(self.pipelineDict.items())[0][0]
            self.pipelineSetText(firstPipeline)
        except Exception as e:
            print(e)

    def saveFile(self):
        try:
            if self.save == False:
                self.getInput()
                self.pipelineDict[self.listWidget_2.currentItem().text()] = self.execCode
                self.filename, status = QtWidgets.QFileDialog.getSaveFileName(self,
                    'Open File','',"All Files (*);;Log Files (*.log)", "Log Files (*.log)")
                with open(self.filename, 'w') as f:
                    pipelineFile = json.dumps(self.pipelineDict)
                    f.write(pipelineFile)
                self.save = True
            else:
                self.getInput()
                self.pipelineDict[self.listWidget_2.currentItem().text()] = self.execCode
                with open(self.filename, 'w') as f:
                    pipelineFile = json.dumps(self.pipelineDict)
                    f.write(pipelineFile)
        except Exception as e:
            pass

    def saveFileAs(self):
        try:
            self.filename, status = QtWidgets.QFileDialog.getSaveFileName(self,
                                                                          "Save file as",
                                                                          '',
                                                                          "All Files(*)",
                                                                          "All Files(*)")
            with open(self.filename, 'w') as f:
                pipelineFile = json.dumps(self.pipelineDict)
                f.write(pipelineFile)

        except:
            pass

    '''
    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(
            self, 'Message', 'Are you sure to quit ?',
            QtWidgets.QMessageBox.Yes | 
            QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    '''

