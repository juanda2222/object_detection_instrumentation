import functools
import sys
import traceback

#local libraries 
from temporal_extraction import Temporal_extract
from energy_extraction import Energy_signal
from get_data import get_data
from frecuency_extraction import Frecuency_extraction
from extract_features import Extract_features
from save_object import save_object
from neural_network import neural_network


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
        
        # Add de navigation event handlers:
        self.window.back.clicked.connect(partial(self.navigationHandler, "back"))
        self.window.next.clicked.connect(partial(self.navigationHandler, "next"))

        # Add de event handlers to the configuration page:
        self.window.captureData.clicked.connect(partial(self.capture_data_function))
        self.window.SaveObject.clicked.connect(partial(self.saveObjectHandler))      
        self.window.t1r1Enable.stateChanged.connect(partial(self.configureSensor,"t1r1"))
        self.window.t1r2Enable.stateChanged.connect(partial(self.configureSensor,"t1r2"))
        self.window.t2r1Enable.stateChanged.connect(partial(self.configureSensor,"t2r1"))
        self.window.t2r2Enable.stateChanged.connect(partial(self.configureSensor,"t2r2"))

        # Add de event handlers to the configuration page:
        self.window.identifyButton.clicked.connect(partial(self.identify_fuction))

        #configuration graphics
        self.my_plot_t1r1 = singlePlot2D("Response 1", self.window.t1r1Graph)
        self.my_plot_t1r2 = singlePlot2D("Response 2", self.window.t1r2Graph)
        self.my_plot_t2r1 = singlePlot2D("Response 3", self.window.t2r1Graph)
        self.my_plot_t2r2 = singlePlot2D("Response 4", self.window.t2r2Graph)
        
        self.my_plot_multi = multiPlot2D("Response", self.window.detectionGraph)


        #from the configuration pdu:
        self.frec_muestreo = 8928

        self.window.show()
        print("view init done!")


    def navigationHandler(self, direction):
        index = self.window.stacked_windows.currentIndex()
        
        if direction == "back":
            self.window.stacked_windows.setCurrentIndex(index-1)
            print("back")
        elif direction == "next":
            self.window.stacked_windows.setCurrentIndex(index+1)
            print("next")


    def saveObjectHandler (self):
        global save         
        global name
        #show the message window:
        msgBox = QtGui.QMessageBox()
        msgBox.setText("Prepare your Object")
        msgBox.setInformativeText("¿Do you have your object on front of the sensor?")
        msgBox.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.Cancel)
        msgBox.setDefaultButton(QtGui.QMessageBox.Yes)
        ret = msgBox.exec_()
        
        if ret == QtGui.QMessageBox.Yes:    
            
            # Save was clicked
            name_object = self.window.lineEdit.text()
            print("save pressed")
            print ("object saved as: ",name_object)
            save_object(dF,dT,E,name_object)


        elif ret == QtGui.QMessageBox.Cancel:
            # cancel was clicked
            save = 0
            print("canceled pressed")     
        else:
            print("canceled")

        

    def get_dat(self):
        #get the data:
        self.s1,self.s2,self.s3,self.s4=get_data()
        self.num_datos = np.arange(len(self.s1))
        self.t = self.num_datos*(1/self.frec_muestreo)
        return (self.s1, self.s2, self.s3, self.s4)


    def configureSensor(self,data,state):
        global t1r1
        global t1r2
        global t2r1
        global t2r2
        if data == "t1r1":
            if state == QtCore.Qt.Checked: 
                t1r1 = 1 
            else:
                t1r1 = 0
        if data == "t1r2":
            if state == QtCore.Qt.Checked: 
                t1r2 = 1      
            else:
                t1r2 = 0      
        if data == "t2r1":
            if state == QtCore.Qt.Checked: 
                t2r1 = 1      
            else:
                t2r1 = 0
        if data == "t2r2":
            if state == QtCore.Qt.Checked: 
                t2r2 = 1     
            else:
                t2r2 = 0


    def capture_data_function(self):
        global dF
        global dT
        global E
        #get the data:
        vecs = self.get_dat()

        #save the characteristics on the vectors:
        self.signal = Extract_features()

        self.FrecuencyFactorVector1 = self.signal.frecuency_extraction(vecs[0],self.frec_muestreo)   
        self.timeFactorVector1 = 1000*self.signal.temporal_extraction(vecs[0],self.frec_muestreo)
        self.CombinedFactorVector1 = self.signal.energy_extraction(vecs[0])

        self.FrecuencyFactorVector2 = self.signal.frecuency_extraction(vecs[1],self.frec_muestreo)   
        self.timeFactorVector2 = 1000*self.signal.temporal_extraction(vecs[1],self.frec_muestreo)
        self.CombinedFactorVector2 = self.signal.energy_extraction(vecs[1])

        self.FrecuencyFactorVector3 = self.signal.frecuency_extraction(vecs[2],self.frec_muestreo)   
        self.timeFactorVector3 = 1000*self.signal.temporal_extraction(vecs[2],self.frec_muestreo)
        self.CombinedFactorVector3 = self.signal.energy_extraction(vecs[2])

        self.FrecuencyFactorVector4 = self.signal.frecuency_extraction(vecs[3],self.frec_muestreo)   
        self.timeFactorVector4 = 1000*self.signal.temporal_extraction(vecs[3],self.frec_muestreo)
        self.CombinedFactorVector4 = self.signal.energy_extraction(vecs[3])

        if t1r1 == 1 and t1r2 == 0 and t2r1 == 0 and t2r2 == 0 :
            
            #show the results of the algorithm on each plot:
            self.window.t1r1Time.display(self.timeFactorVector1)
            self.window.t1r1Frecuency.display(self.FrecuencyFactorVector1)
            self.window.t1r1Combined.display(self.CombinedFactorVector1)

            #graficate each response:
            self.my_plot_t1r1.update_data(self.t, vecs[0])

            dF = self.FrecuencyFactorVector1
            dT = self.timeFactorVector1
            E = self.CombinedFactorVector1

        if t1r1 == 1 and t1r2 == 1 and t2r1 == 0 and t2r2 == 0 :
            
            #show the results of the algorithm on each plot:
            self.window.t1r1Time.display(self.timeFactorVector1)
            self.window.t1r1Frecuency.display(self.FrecuencyFactorVector1)
            self.window.t1r1Combined.display(self.CombinedFactorVector1)

            self.window.t1r2Time.display(self.timeFactorVector2)
            self.window.t1r2Frecuency.display(self.FrecuencyFactorVector2)
            self.window.t1r2Combined.display(self.CombinedFactorVector2)

            #graficate each response:
            self.my_plot_t1r1.update_data(self.t, vecs[0])
            self.my_plot_t1r2.update_data(self.t, vecs[1])

            dF = (self.FrecuencyFactorVector1+self.FrecuencyFactorVector2)/2
            dT = (self.timeFactorVector1+self.timeFactorVector2)/2
            E = (self.CombinedFactorVector1+self.CombinedFactorVector2)/2

        if t1r1 == 1 and t1r2 == 0 and t2r1 == 1 and t2r2 == 0 :
            
            #show the results of the algorithm on each plot:
            self.window.t1r1Time.display(self.timeFactorVector1)
            self.window.t1r1Frecuency.display(self.FrecuencyFactorVector1)
            self.window.t1r1Combined.display(self.CombinedFactorVector1)

            self.window.t2r1Time.display(self.timeFactorVector3)
            self.window.t2r1Frecuency.display(self.FrecuencyFactorVector3)
            self.window.t2r1Combined.display(self.CombinedFactorVector3) 

            #graficate each response:
            self.my_plot_t1r1.update_data(self.t, vecs[0])
            self.my_plot_t2r1.update_data(self.t, vecs[2])

            dF = (self.FrecuencyFactorVector1+self.FrecuencyFactorVector3)/2
            dT = (self.timeFactorVector1+self.timeFactorVector3)/2
            E = (self.CombinedFactorVector1+self.CombinedFactorVector3)/2

        if t1r1 == 1 and t1r2 == 1 and t2r1 == 1 and t2r2 == 1 :
            
            #show the results of the algorithm on each plot:
            self.window.t1r1Time.display(self.timeFactorVector1)
            self.window.t1r1Frecuency.display(self.FrecuencyFactorVector1)
            self.window.t1r1Combined.display(self.CombinedFactorVector1)

            self.window.t1r2Time.display(self.timeFactorVector2)
            self.window.t1r2Frecuency.display(self.FrecuencyFactorVector2)
            self.window.t1r2Combined.display(self.CombinedFactorVector2)

            self.window.t2r1Time.display(self.timeFactorVector3)
            self.window.t2r1Frecuency.display(self.FrecuencyFactorVector3)
            self.window.t2r1Combined.display(self.CombinedFactorVector3) 

            self.window.t2r2Time.display(self.timeFactorVector4)
            self.window.t2r2Frecuency.display(self.FrecuencyFactorVector4)
            self.window.t2r2Combined.display(self.CombinedFactorVector4)

            #graficate each response:
            self.my_plot_t1r1.update_data(self.t, vecs[0])
            self.my_plot_t1r2.update_data(self.t, vecs[1])
            self.my_plot_t2r1.update_data(self.t, vecs[2])
            self.my_plot_t2r2.update_data(self.t, vecs[3])

            dF = (self.FrecuencyFactorVector1+self.FrecuencyFactorVector2+self.FrecuencyFactorVector3+self.FrecuencyFactorVector4)/4
            dT = (self.timeFactorVector1+self.timeFactorVector2+self.timeFactorVector3+self.timeFactorVector4)/4
            E = (self.CombinedFactorVector1+self.CombinedFactorVector2+self.CombinedFactorVector3+self.CombinedFactorVector4)/4

        print("data adquired")

       
    def identify_fuction(self):
        vecs = self.get_dat()
        self.my_plot_multi.update_data(self.t, vecs)

        #save the characteristics on the vectors:
        self.signal = Extract_features()

        self.FrecuencyFactorVector1 = self.signal.frecuency_extraction(vecs[0],self.frec_muestreo)   
        self.timeFactorVector1 = 1000*self.signal.temporal_extraction(vecs[0],self.frec_muestreo)
        self.CombinedFactorVector1 = self.signal.energy_extraction(vecs[0])

        self.FrecuencyFactorVector2 = self.signal.frecuency_extraction(vecs[1],self.frec_muestreo)   
        self.timeFactorVector2 = 1000*self.signal.temporal_extraction(vecs[1],self.frec_muestreo)
        self.CombinedFactorVector2 = self.signal.energy_extraction(vecs[1])

        self.FrecuencyFactorVector3 = self.signal.frecuency_extraction(vecs[2],self.frec_muestreo)   
        self.timeFactorVector3 = 1000*self.signal.temporal_extraction(vecs[2],self.frec_muestreo)
        self.CombinedFactorVector3 = self.signal.energy_extraction(vecs[2])

        self.FrecuencyFactorVector4 = self.signal.frecuency_extraction(vecs[3],self.frec_muestreo)   
        self.timeFactorVector4 = 1000*self.signal.temporal_extraction(vecs[3],self.frec_muestreo)
        self.CombinedFactorVector4 = self.signal.energy_extraction(vecs[3])   

        if t1r1 == 1 and t1r2 == 0 and t2r1 == 0 and t2r2 == 0 :
            
            dF = self.FrecuencyFactorVector1
            dT = self.timeFactorVector1
            E = self.CombinedFactorVector1

        if t1r1 == 1 and t1r2 == 1 and t2r1 == 0 and t2r2 == 0 :        

            dF = (self.FrecuencyFactorVector1+self.FrecuencyFactorVector2)/2
            dT = (self.timeFactorVector1+self.timeFactorVector2)/2
            E = (self.CombinedFactorVector1+self.CombinedFactorVector2)/2

        if t1r1 == 1 and t1r2 == 0 and t2r1 == 1 and t2r2 == 0 :
            
            dF = (self.FrecuencyFactorVector1+self.FrecuencyFactorVector3)/2
            dT = (self.timeFactorVector1+self.timeFactorVector3)/2
            E = (self.CombinedFactorVector1+self.CombinedFactorVector3)/2

        if t1r1 == 1 and t1r2 == 1 and t2r1 == 1 and t2r2 == 1 :

            dF = (self.FrecuencyFactorVector1+self.FrecuencyFactorVector2+self.FrecuencyFactorVector3+self.FrecuencyFactorVector4)/4
            dT = (self.timeFactorVector1+self.timeFactorVector2+self.timeFactorVector3+self.timeFactorVector4)/4
            E = (self.CombinedFactorVector1+self.CombinedFactorVector2+self.CombinedFactorVector3+self.CombinedFactorVector4)/4

        #percentaje object 
        p_ob1,p_ob2,p_ob3,name_object = neural_network(dF,dT,E)

        #show the results of the algorithm on each plot:
        self.window.object1_result.display(p_ob1)
        self.window.object2_result.display(p_ob2)
        self.window.object3_result.display(p_ob3)
        self.window.objectName_result.setText(name_object)
        
        print("data adquired")


class singlePlot2D(pg.GraphicsWindow):
    def __init__(self, graphName, widget):
        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)

        # for the inheritance specifications:
        super(singlePlot2D, self).__init__(parent=widget)

        # to add this widget to the widget parent:
        layout = pg.QtGui.QVBoxLayout()
        widget.setLayout(layout)
        # self.setParent(widget)
        layout.addWidget(self)

        self.myPlot = self.addPlot()
        #self.myPlot.setLabels(left='v')
        self.myPlot.setLabels(bottom='tiempo')

        self.newLine = self.myPlot.plot(pen = {'color': (0,85,127), 'width': 2} )

    def update_data(self, x_vector, y_vector):
        self.newLine.setData(x_vector, y_vector)


class multiPlot2D(pg.GraphicsWindow):
    def __init__(self, graphName, widget):
        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)

        # for the inheritance specifications:
        super(multiPlot2D, self).__init__(parent=widget)

        # for custom class managment:
        self.t = np.arange(0, 3.0, 0.01)

        self.a = []
        self.b = []
        self.c = []
        self.d = []

        # to add this widget to the widget parent:
        layout = pg.QtGui.QVBoxLayout()
        widget.setLayout(layout)
        # self.setParent(widget)
        layout.addWidget(self)

        self.myPlot = self.addPlot(title = graphName)
        #self.myPlot.setLabels(left='Valor')
        self.myPlot.setLabels(bottom='tiempo')

        self.traceT1R1 = self.myPlot.plot(pen = {'color': (255,115,117), 'width': 2} )
        self.traceT1R2 = self.myPlot.plot(pen = {'color': (58,117,255), 'width': 2} )
        self.traceT2R1 = self.myPlot.plot(pen = {'color': (255,255,116), 'width': 2} )
        self.traceT2R2 = self.myPlot.plot(pen = {'color': (243,255,213), 'width': 2} )


    def update_data(self, dataset_x, datasets_y):
        if t1r1 == 1 and t1r2 == 0 and t2r1 == 0 and t2r2 == 0 :
            
            self.traceT1R1.setData(dataset_x, datasets_y[0])

        if t1r1 == 1 and t1r2 == 1 and t2r1 == 0 and t2r2 == 0 :        

            self.traceT1R1.setData(dataset_x, datasets_y[0])
            self.traceT1R2.setData(dataset_x, datasets_y[1])

        if t1r1 == 1 and t1r2 == 0 and t2r1 == 1 and t2r2 == 0 :
            
            self.traceT1R1.setData(dataset_x, datasets_y[0])
            self.traceT2R1.setData(dataset_x, datasets_y[2])

        if t1r1 == 1 and t1r2 == 1 and t2r1 == 1 and t2r2 == 1 :

            self.traceT1R1.setData(dataset_x, datasets_y[0])
            self.traceT1R2.setData(dataset_x, datasets_y[1])
            self.traceT2R1.setData(dataset_x, datasets_y[2])
            self.traceT2R2.setData(dataset_x, datasets_y[3]) 