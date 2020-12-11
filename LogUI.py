from PyQt5 import QtWidgets, QtGui

class logUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(logUI, self).__init__()
        self.init_ui()
        
    def init_ui(self):
        
        
        self.resize(800, 600)
        self.setWindowTitle("Running Results")
        
        self.textB = QtWidgets.QTextBrowser()
        self.textB.setText("This is a log file !")
        
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.textB.setFont(font)
        
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # add widget
        layout.addWidget(self.textB)
        
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
        # menu bar
        self.menuBar = self.menuBar()
        
        #exitAct = QtWidgets.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exitAct = QtWidgets.QAction('&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.close)

        saveAct = QtWidgets.QAction('&Save', self)
        saveAct.setShortcut('Ctrl+S')
        saveAct.setStatusTip('Save log file')
        saveAct.triggered.connect(self.saveFile)

        self.fileMenu = self.menuBar.addMenu('&File')
        self.fileMenu.addAction(exitAct)
        self.fileMenu.addAction(saveAct)
        
        #status bar
        self.statusBar = self.statusBar()
        self.statusBar.showMessage("Running log", 0)
        
    def saveFile(self):
        filename, status = QtWidgets.QFileDialog.getSaveFileName(self,\
           'Save File','',"All Files (*);;Log Files (*.log)", "Log Files (*.log)")
        with open(filename,'w') as f:
            text = self.textB.toPlainText()
            f.write(text)
        

