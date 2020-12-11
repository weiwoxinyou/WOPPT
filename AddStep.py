# -*- coding: utf-8 -*-


from PyQt5 import QtWidgets, QtGui

class addStep(QtWidgets.QWidget):
    def __init__(self):
        super(addStep, self).__init__()
        self.initUI()
        
    def initUI(self):
        
        # sw refers to software, sc refers to script, pm refers to parameter
        
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        
        # basic setting
        self.lineEditsw = QtWidgets.QLineEdit(self)
        self.lineEditsw.setPlaceholderText("Choose your software")
        
        self.lineEditsc = QtWidgets.QLineEdit(self)
        self.lineEditsc.setPlaceholderText("Choose your script")
        
        self.lineEditpm = QtWidgets.QLineEdit(self)
        self.lineEditpm.setPlaceholderText("Additional parameter, default None")
        
        self.toolButtonsw = QtWidgets.QToolButton(self)
        self.toolButtonsw.setText("...")
        
        self.toolButtonsc = QtWidgets.QToolButton(self)
        self.toolButtonsc.setText("...")
        
        self.labelsw = QtWidgets.QLabel(self)
        self.labelsw.setText("Software:")
        
        self.labelsc = QtWidgets.QLabel(self)
        self.labelsc.setText("Script:")
        
        self.labelpm = QtWidgets.QLabel(self)
        self.labelpm.setText("Parameter:")
        
        self.inputFile = QtWidgets.QLineEdit(self)
        self.inputFile.setPlaceholderText("Input file")

        self.outputFile = QtWidgets.QLineEdit(self)
        self.outputFile.setPlaceholderText("Output file")
        
        self.labelsw.setFont(font)
        self.labelsc.setFont(font)
        self.labelpm.setFont(font)
        
        self.labelsw.setBuddy(self.lineEditsw)
        self.labelsc.setBuddy(self.lineEditsc)
        self.labelpm.setBuddy(self.lineEditpm)
        
        
        # set the horizontal layout
        self.gridLayout = QtWidgets.QHBoxLayout(self)
        
        self.gridLayout.addWidget(self.labelsw)
        self.gridLayout.addWidget(self.lineEditsw)
        self.gridLayout.addWidget(self.toolButtonsw)
        
        self.gridLayout.addWidget(self.labelsc)
        self.gridLayout.addWidget(self.lineEditsc)
        self.gridLayout.addWidget(self.toolButtonsc)
        
        self.gridLayout.addWidget(self.inputFile)
        self.gridLayout.addWidget(self.outputFile)
        
        self.gridLayout.addWidget(self.labelpm)
        self.gridLayout.addWidget(self.lineEditpm)
        
        
        # bind to file choose
        self.toolButtonsw.clicked.connect(self.getName1)
        self.toolButtonsc.clicked.connect(self.getName2)
        
        
    def getName1(self):
        # print(self.__class__.__name__)
        filepath, filytype = QtWidgets.QFileDialog.getOpenFileName(self, "Choose a File")
        try:
            self.path1 = filepath
            self.lineEditsw.setText(self.path1)
        except Exception as e:
            print(e)
        
    def getName2(self):
        filepath, filytype = QtWidgets.QFileDialog.getOpenFileName(self, "Choose a File")
        try:
            self.path1 = filepath
            self.lineEditsc.setText(self.path1)
        except Exception as e:
            print(e)
        



