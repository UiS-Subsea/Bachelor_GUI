# Form implementation generated from reading ui file 'd:\Bachelor_GUI\GUI\temperatur.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tempLabel = QtWidgets.QLabel(self.centralwidget)
        self.tempLabel.setGeometry(QtCore.QRect(300, 310, 311, 161))
        self.tempLabel.setObjectName("tempLabel")
        self.dangerButton = QtWidgets.QPushButton(self.centralwidget)
        self.dangerButton.setGeometry(QtCore.QRect(307, 186, 201, 121))
        self.dangerButton.setObjectName("dangerButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tempLabel.setText(_translate("MainWindow", "TemperaturTest"))
        self.dangerButton.setText(_translate("MainWindow", "DANGER!"))
