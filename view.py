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
        
        # Add de event handlers to the configuration page:
        self.window.captureData.clicked.connect(partial(self.capture_data_function))
        self.window.object1Save.clicked.connect(partial(self.saveObjectHandler, "1"))      
        self.window.object2Save.clicked.connect(partial(self.saveObjectHandler, "2"))
        self.window.object3Save.clicked.connect(partial(self.saveObjectHandler, "3"))
        self.window.t1r1Enable.stateChanged.connect(partial(self.configureSensor,"t1r1"))
        self.window.t1r2Enable.stateChanged.connect(partial(self.configureSensor,"t1r2"))
        self.window.t2r1Enable.stateChanged.connect(partial(self.configureSensor,"t2r1"))
        self.window.t2r2Enable.stateChanged.connect(partial(self.configureSensor,"t2r2"))

        # graphics
        self.my_plot_t1r1 = singlePlot2D("Response 1", self.window.t1r1Graph)
        self.my_plot_t1r2 = singlePlot2D("Response 2", self.window.t1r2Graph)
        self.my_plot_t2r1 = singlePlot2D("Response 3", self.window.t2r1Graph)
        self.my_plot_t2r2 = singlePlot2D("Response 4", self.window.t2r2Graph)

        #from the configuration pdu:
        self.frec_muestreo = 2000
        self.numBits_dato = 8
        self.ref_volt = 4

        #From each data pack:
        self.num_datos = 100
        self.ganancia = 200

        self.window.show()
        print("view init done!")

    def configureSensor(self):
        pass

    def saveObjectHandler (self, object_to_save):
        
        #get the data

        #show the message window:
        msgBox = QtGui.QMessageBox()
        msgBox.setText("Prepare your Object")
        msgBox.setInformativeText("¿Do you have your object on front of the sensor?")
        msgBox.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.Cancel)
        msgBox.setDefaultButton(QtGui.QMessageBox.Yes)
        ret = msgBox.exec_()
        
        if ret == QtGui.QMessageBox.Yes:
            # Save was clicked
            print("save pressed")
        elif ret == QtGui.QMessageBox.Cancel:
            # cancel was clicked
             print("canceled pressed")     
        else:
            print("canceled")

        if object_to_save == "1":
            print ("object 1 saved as: "+self.window.object1Name)
        elif object_to_save == "2":
            print ("object 2 saved as: "+self.window.object2Name)
        elif object_to_save == "3":
            print ("object 3 saved as: "+self.window.object3Name)

        

    def capture_data_function(self):
        
        #get the data:
        sine_freq = 60
        self.n = np.arange(self.num_datos)
        self.t = self.n*(1/self.frec_muestreo)
        self.s1 = sin(2 * pi * sine_freq * self.t) + (np.random.rand(self.num_datos))/3
        self.s2 = sin(2 * pi * sine_freq * self.t) + (np.random.rand(self.num_datos))/3
        self.s3 = sin(2 * pi * sine_freq * self.t) + (np.random.rand(self.num_datos))/3
        self.s4 = sin(2 * pi * sine_freq * self.t) + (np.random.rand(self.num_datos))/3

        #graficate each response:
        self.my_plot_t1r1.update_data(self.t, self.s1)
        self.my_plot_t1r2.update_data(self.t, self.s2)
        self.my_plot_t2r1.update_data(self.t, self.s3)
        self.my_plot_t2r2.update_data(self.t, self.s4)

        #save the characteristics on the vectors:
        self.timeFactorVector = np.random.rand(4)
        self.FrecuencyFactorVector = np.random.rand(4)
        self.CombinedFactorVector = np.random.rand(4)

        #show the results of the algorithm
        self.window.t1r1Time.display(self.timeFactorVector[0])
        self.window.t1r1Frecuency.display(self.FrecuencyFactorVector[0])
        self.window.t1r1Combined.display(self.CombinedFactorVector[0])

        self.window.t1r2Time.display(self.timeFactorVector[1])
        self.window.t1r2Frecuency.display(self.FrecuencyFactorVector[1])
        self.window.t1r2Combined.display(self.CombinedFactorVector[1])

        self.window.t2r1Time.display(self.timeFactorVector[2])
        self.window.t2r1Frecuency.display(self.FrecuencyFactorVector[2])
        self.window.t2r1Combined.display(self.CombinedFactorVector[2])
        
        self.window.t2r2Time.display(self.timeFactorVector[3])
        self.window.t2r2Frecuency.display(self.FrecuencyFactorVector[3])
        self.window.t2r2.Combined.display(self.CombinedFactorVector[3])

        print("data adquired")




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

        self.myPlot = self.addPlot()
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