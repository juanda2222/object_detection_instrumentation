import functools
import sys
import traceback



# for gui tools:
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtUiTools import *
from PySide2.QtUiTools import *
from PySide2 import QtUiTools

import pyqtgraph as pg
# for plotting:
#import matplotlib


import numpy as np
#from PySide.QtGui import QVBoxLayout
from numpy import arange, sin, cos, pi

# aditional tools:
from functools import partial  # para facilitar el manejo de eventos


class View(QtCore.QObject):  # hereda de la clase QtGui.QmainWindow

    def __init__(self, ui_file_path, controller):

        # ------------basic configuration:------------------

        super(View, self).__init__(parent=None)  # initialize the parent class (QtGui)
        self.controller = controller

        # load ui file:
        loader = QtUiTools.QUiLoader()
        my_file = QtCore.QFile(ui_file_path)
        my_file.open(QtCore.QFile.ReadOnly)
        self.window = loader.load(my_file)
        my_file.close()

        # window configuration:
        self.window.setWindowIcon(QtGui.QIcon("./icons/icon.png"))  # el punto significa el lugar donde esta el script
        
        # Add de event handlers to de menu objects
        self.window.captureData.clicked.connect(partial(self.capture_data_function, "paaapuuuu"))       

        # graphics
        self.my_plot_t1r1 = singlePlot2D("Response 1", self.window.t1r1Graph)
        self.my_plot_t1r2 = singlePlot2D("Response 2", self.window.t1r2Graph)
        self.my_plot_t2r1 = singlePlot2D("Response 3", self.window.t2r1Graph)
        self.my_plot_t2r2 = singlePlot2D("Response 4", self.window.t2r2Graph)

        #from the configuration pdu:
        self.frec_muestreo = 100
        self.numBits_dato = 8
        self.ref_volt = 4
        self.n = np.arange(self.num_datos)
        self.t = self.n*(1/self.frec_muestreo)

        #From each data pack:
        self.num_datos = 1000
        self.ganancia = 200

        sine_freq = 60
        self.s = sin(2 * pi * sine_freq * self.t)
        

        self.window.show()
        print("view init done!")

    def capture_data_function(self, arguments):
        print("change_mode_check pressed")

        #show the message window:
        dial = QtGui.QMessageBox()
        dial.setText(u"Delete all selected paths?")
        dial.setWindowTitle("the name stored is: "+arguments)
        yesBt = dial.addButton('Yes', QtGui.QMessageBox.YesRole)
        noBt = dial.addButton('No', QtGui.QMessageBox.NoRole)
        dial.exec_()
        
        if dial.clickedButton() == yesBt:
            print("yes pressed")
        if dial.clickedButton() == noBt:
            print("no pressed")
        else:
            print("canceled")

        print(arguments)


class singlePlot2D(pg.GraphicsWindow):
    def __init__(self, graphName, widget):
        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)

        #pg.setConfigOption('background', 'w')
        #pg.setConfigOption('foreground', 'k')

        # for the inheritance specifications:
        super(singlePlot2D, self).__init__(parent=widget)

        # to add this widget to the widget parent:
        layout = pg.QtGui.QVBoxLayout()
        widget.setLayout(layout)
        # self.setParent(widget)
        layout.addWidget(self)

        #self.plot_space.setWindowTitle('pyqtgraph example: Scrolling Plots')

        self.myPlot = self.addPlot(title = graphName)
        self.myPlot.setLabels(left='Valor')
        self.myPlot.setLabels(bottom='tiempo')

        self.newLine = self.myPlot.plot(pen = {'color': (255,0,0), 'width': 2} )

    def update_data(self, x_vector, y_vector):
        self.newLine.setData(x_vector, y_vector)




class multiPlot2D(pg.GraphicsWindow):
    def __init__(self, graphName, widget):
        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)

        #pg.setConfigOption('background', 'w')
        #pg.setConfigOption('foreground', 'k')

        # for the inheritance specifications:
        super(multiPlot2D, self).__init__(parent=widget)

        # for custom class managment:
        self.t = np.arange(0, 3.0, 0.01)
        self.s = []
        self.c = []
        self.i = 0  # this is the variable which contain the steps done by the time axis
        self.traces = dict()
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_data)

        # to add this widget to the widget parent:
        layout = pg.QtGui.QVBoxLayout()
        widget.setLayout(layout)
        # self.setParent(widget)
        layout.addWidget(self)

        #self.plot_space.setWindowTitle('pyqtgraph example: Scrolling Plots')

        self.myPlot = self.addPlot(title = graphName)
        self.myPlot.setLabels(left='Valor')
        self.myPlot.setLabels(bottom='tiempo')

        ## set pen on a single data set:
        #plotline.setPen(color=(255, 0, 0), width=3)



    def start(self):
        self.timer.start(10)

    def trace(self, name, dataset_x, dataset_y):
        if name in self.traces:
            self.traces[name].setData(dataset_x, dataset_y)
        else:
            self.traces[name] = self.myPlot.plot(pen = {'color': (255,0,0), 'width': 3} )

    def update_data(self):
        self.s = sin(2 * pi * self.t + self.i)
        self.c = cos(2 * pi * self.t + self.i)
        self.trace("sin", self.t, self.s)
        self.trace("cos", self.t, self.c)
        self.i += 0.1