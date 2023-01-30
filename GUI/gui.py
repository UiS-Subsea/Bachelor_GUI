import sys
from PyQt6 import QtWidgets, uic
from pyqtgraph import PlotWidget
import pyqtgraph as pg


class MainWindow(QtWidgets.QMainWindow):
    def __init(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi("mainwindow.ui", self)

        self.show()

        self.plot([1,2,3,4,5,6,7,8,9,10], [30,32,34,32,33,31,29,32,35,45])
        
        def plot(self, hour, temperature):
            self.graphWidget.plot(hour, temperature)


app = QtWidgets.QApplication(sys.argv)

window = uic.loadUi("mainwindow.ui")
window.show()
app.exec()
