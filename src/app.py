from PyQt5 import QtCore, QtGui, QtWidgets
import translation
import constants

class Worker(QtCore.QRunnable):

    def __init__(self, *args):
        super(Worker, self).__init__()
        self.args = args
    
    def run(self):
        print("Thread start")
        print(self.args[0] + " " + self.args[1])
        translation.threadedAndBetter2(self.args[0], self.args[1])  # calls the new translator in the desired thread
        print("Thread complete")

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # UI SETUP
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(568, 200)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.nativeLanguage = QtWidgets.QComboBox(self.centralwidget)
        self.nativeLanguage.setGeometry(QtCore.QRect(50, 60, 131, 21))
        self.nativeLanguage.setObjectName("nativeLanguage")
        self.nativeLanguage.addItems(constants.langs.keys())
        self.translateButton = QtWidgets.QPushButton(self.centralwidget)
        self.translateButton.setGeometry(QtCore.QRect(310, 70, 201, 51))
        self.translateButton.setObjectName("translateButton")
        self.translateButton.setText("Translate")
        self.targetLanguage = QtWidgets.QComboBox(self.centralwidget)
        self.targetLanguage.setGeometry(QtCore.QRect(50, 130, 131, 21))
        self.targetLanguage.setObjectName("targetLanguage")
        self.targetLanguage.addItems(constants.langs2.keys())
        self.fromLabel = QtWidgets.QLabel(self.centralwidget)
        self.fromLabel.setGeometry(QtCore.QRect(50, 40, 47, 13))
        self.fromLabel.setObjectName("fromLabel")
        self.toLabel = QtWidgets.QLabel(self.centralwidget)
        self.toLabel.setGeometry(QtCore.QRect(50, 110, 47, 13))
        self.toLabel.setObjectName("toLabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        self.nativeLanguage.setCurrentIndex(0)
        self.targetLanguage.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.worker = Worker(self.nativeLanguage.currentText(), self.targetLanguage.currentText())

        # BINDINGS
            # Translate Button
        self.translateButton.clicked.connect(self.clicked)

        # MISC
        self.threadpool = QtCore.QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Translator"))
        self.fromLabel.setText(_translate("MainWindow", "From"))
        self.toLabel.setText(_translate("MainWindow", "To"))

    # BUTTON CLICKED EVENT
    def clicked(self):
        self.worker = Worker(self.nativeLanguage.currentText(), self.targetLanguage.currentText())
        if (self.translateButton.text() == "Translate"):
            self.translateButton.setText("Stop Translating")
            self.threadpool.start(self.worker)  # opens new translating thread
        else:
            self.translateButton.setText("Translate")
        # new thread start

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()        
    sys.exit(app.exec_())
