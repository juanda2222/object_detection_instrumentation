import functools
import sys
import traceback
import numpy as np
import random

#local libraries 
from temporal_extraction import Temporal_extract
from energy_extraction import Energy_signal
from get_data import get_data

from myNeural import Neural_Network
from temporal_extraction import get_butter_lowpass_coef
from temporal_extraction import butter_lowpass_filter

from frecuency_extraction import Frecuency_extraction
from extract_features import Extract_features

# neural network de jaime
from neural_lib import Neural_lib


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

MODE_T1R1 = 1
MODE_T1R2 = 2
MODE_T2R1 = 3
MODE_T2R2 = 4
MODE_NONE = 5

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
        self.window.setWindowIcon(QtGui.QIcon("./icons/icon.jpg"))  # el punto significa el lugar donde esta el script
                
        # Add de navigation event handlers:
        self.window.back.clicked.connect(partial(self.navigationHandler, "back"))
        self.window.next.clicked.connect(partial(self.navigationHandler, "next"))

        # Add de event handlers to the configuration page:
        self.window.captureData.clicked.connect(partial(self.capture_data_function))
        self.window.object1Save.clicked.connect(partial(self.saveObjectHandler, "1"))      
        self.window.object2Save.clicked.connect(partial(self.saveObjectHandler, "2"))
        self.window.object3Save.clicked.connect(partial(self.saveObjectHandler, "3"))

        self.window.t1r1Enable.stateChanged.connect(partial(self.configureSensor, "t1r1"))
        self.window.t1r2Enable.stateChanged.connect(partial(self.configureSensor, "t1r2"))
        self.window.t2r1Enable.stateChanged.connect(partial(self.configureSensor, "t2r1"))
        self.window.t2r2Enable.stateChanged.connect(partial(self.configureSensor, "t2r2"))

        # Add de event handlers to the identification page:
        self.window.identifyButton.clicked.connect(partial(self.identify_fuction))

        #configuration graphics
        self.my_plot_t1r1 = singlePlot2D("Response 1", self.window.t1r1Graph)
        self.my_plot_t1r2 = singlePlot2D("Response 2", self.window.t1r2Graph)
        self.my_plot_t2r1 = singlePlot2D("Response 3", self.window.t2r1Graph)
        self.my_plot_t2r2 = singlePlot2D("Response 4", self.window.t2r2Graph)
        
        self.my_plot_multi = multiPlot2D("Response", self.window.detectionGraph)

        # the type of sensor would be saved in a sible variable (macros in the beginning)
        self.sensorType = MODE_T2R2
        self.object_Name = ["None", "None", "None"] # list of names
        # initialize the current characteristics buffer
        self.empty_characteristics_buffer(1)
        self.empty_characteristics_buffer(2)
        self.empty_characteristics_buffer(3)
        self.empty_characteristics_buffer(4)

        self.vec_objetos = [{
                "timeFactorVector"  : None,
                "FrecuencyFactorVector" : None,
                "CombinedFactorVector"  : None
            },{
                "timeFactorVector"  : None,
                "FrecuencyFactorVector" : None,
                "CombinedFactorVector"  : None
            },{
                "timeFactorVector" :  None,
                "FrecuencyFactorVector" : None,
                "CombinedFactorVector"  : None
        }]

        # flags used to determined when to train the system
        self.is_object1Saved = False
        self.is_object2Saved = False
        self.is_object3Saved = False
        self.is_neuralTrained = False
        

        #from the configuration pdu:
        self.frec_muestreo = 8928

        #for procesing the data:
        self.t = None #sample rate
        self.num_datos = None #vector size

        # create the  diferent neural networks:
        self.num_trains = 3
        self.num_trains1 = 0
        self.num_trains2 = 0
        self.num_trains3 = 0
        self.neural_t1r1 = Neural_lib(neuralName="t1r1", numIn=3)
        self.neural_t1r2 = Neural_lib(neuralName="t1r2", numIn=6)
        self.neural_t2r1 = Neural_lib(neuralName="t2r1", numIn=6)
        self.neural_t2r2 = Neural_lib(neuralName="t2r2", numIn=12)

        self.window.show()
        print("view init done!")

    def beautify_lcd(self):
        # get the palette
        palette = self.window.t2r2Time.palette()

        # foreground color
        palette.setColor(palette.WindowText, QtGui.QColor(0, 0, 0))
        # background color
        #palette.setColor(palette.Background, QtGui.QColor(0, 170, 255))
        # "light" border
        #palette.setColor(palette.Light, QtGui.QColor(255, 0, 0))
        # "dark" border
        #palette.setColor(palette.Dark, QtGui.QColor(0, 255, 0))

        # set the palette
        self.window.t2r2Time.setPalette(palette)

    def empty_characteristics_buffer(self, channel):
        #clean the buffer depending on the need
        if channel == 1:
            self.FrecuencyFactorVector1 = 0
            self.timeFactorVector1 = 0
            self.CombinedFactorVector1 = 0
        elif channel == 2:
            self.FrecuencyFactorVector2 = 0
            self.timeFactorVector2 = 0
            self.CombinedFactorVector2 = 0
        elif channel == 3:
            self.FrecuencyFactorVector3 = 0
            self.timeFactorVector3 = 0
            self.CombinedFactorVector3 = 0
        elif channel == 4:
            self.FrecuencyFactorVector4 = 0
            self.timeFactorVector4 = 0
            self.CombinedFactorVector4 = 0
        else:
            print ("Check the selected channel")

    def navigationHandler(self, direction):
        index = self.window.stacked_windows.currentIndex()
        
        if direction == "back":
            self.window.stacked_windows.setCurrentIndex(index-1)
            print("back")
        elif direction == "next":
            self.window.stacked_windows.setCurrentIndex(index+1)
            print("next")

    def saveObjectHandler (self, object_to_save):

        # check problems:
        if  self.sensorType == MODE_NONE:
            msgBox = QtGui.QMessageBox()
            msgBox.setText("check your sensor configuration")
            msgBox.setWindowTitle("Ups, something went wrong")
            ret = msgBox.exec_()
            return
        # the object has no name
        if  (self.window.object1Name.text() == "" and object_to_save == "1") or (
            self.window.object2Name.text() == "" and object_to_save == "2") or (
            self.window.object3Name.text() == "" and object_to_save == "3"
            ): 
            
            msgBox = QtGui.QMessageBox()
            msgBox.setText("please name your object")
            msgBox.setWindowTitle("Ups, something went wrong")
            ret = msgBox.exec_()
            return
        # the data is empty
        if self.timeFactorVector1 == None:
            msgBox = QtGui.QMessageBox()
            msgBox.setText("please capture some data")
            msgBox.setWindowTitle("Ups, something went wrong")
            ret = msgBox.exec_()
            return

        #show the message window:
        msgBox = QtGui.QMessageBox()
        msgBox.setText("Save object")
        msgBox.setWindowTitle("Save this shot")
        msgBox.setInformativeText("¿Are you sure you want to save this object?")
        msgBox.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.Cancel)
        msgBox.setDefaultButton(QtGui.QMessageBox.Yes)
        ret = msgBox.exec_()
        
        if ret == QtGui.QMessageBox.Yes:    

            print("save pressed")

            # save data depending on the object pressed
            if object_to_save == "1":
                print("objeto 1 entro!")

                current_index = 0
                self.num_trains1 += 1 

                # save the text:
                self.object_Name[current_index] = self.window.object1Name.text()
                
                # save the factors:
                self.vec_objetos[0]["timeFactorVector"] = [self.timeFactorVector1, self.timeFactorVector2, self.timeFactorVector3, self.timeFactorVector4]
                self.vec_objetos[0]["FrecuencyFactorVector"] = [self.FrecuencyFactorVector1, self.FrecuencyFactorVector2, self.FrecuencyFactorVector3, self.FrecuencyFactorVector4]
                self.vec_objetos[0]["CombinedFactorVector"] = [self.CombinedFactorVector1, self.CombinedFactorVector2, self.CombinedFactorVector3, self.CombinedFactorVector4]
                
                # display the vector:
                self.window.object1Time.setText(str(np.around(self.vec_objetos[0]["timeFactorVector"], 4)))
                self.window.object1Frecuency.setText(str(np.around(self.vec_objetos[0]["FrecuencyFactorVector"], 4)))
                self.window.object1Combined.setText(str(np.around(self.vec_objetos[0]["CombinedFactorVector"], 3)))
                
                # flag used to determined if its moment to tran the neural network
                self.is_object1Saved = True
                

            elif object_to_save == "2":
                
                print("objeto 2 entró!")

                current_index = 1
                self.num_trains2 += 1 
                
                # save the text:
                self.object_Name[current_index] = self.window.object2Name.text()
                
                # save the factors:
                self.vec_objetos[1]["timeFactorVector"] = [self.timeFactorVector1, self.timeFactorVector2, self.timeFactorVector3, self.timeFactorVector4]
                self.vec_objetos[1]["FrecuencyFactorVector"] = [self.FrecuencyFactorVector1, self.FrecuencyFactorVector2, self.FrecuencyFactorVector3, self.FrecuencyFactorVector4]
                self.vec_objetos[1]["CombinedFactorVector"] = [self.CombinedFactorVector1, self.CombinedFactorVector2, self.CombinedFactorVector3, self.CombinedFactorVector4]

                print("input " + str(self.vec_objetos[0]["timeFactorVector"]))

                # display the vector:
                self.window.object2Time.setText(str(np.around(self.vec_objetos[1]["timeFactorVector"], 4)))
                self.window.object2Frecuency.setText(str(np.around(self.vec_objetos[1]["FrecuencyFactorVector"], 4)))
                self.window.object2Combined.setText(str(np.around(self.vec_objetos[1]["CombinedFactorVector"], 3)))

                # flag used to determined if its moment to tran the neural network
                self.is_object2Saved = True

            elif object_to_save == "3":

                print("objeto 3 entró!")
                current_index = 2
                self.num_trains3 += 1 

                # save the text:
                self.object_Name[current_index] = self.window.object3Name.text()
                
                # save the factors:
                self.vec_objetos[2]["timeFactorVector"] = [self.timeFactorVector1, self.timeFactorVector2, self.timeFactorVector3, self.timeFactorVector4]
                self.vec_objetos[2]["FrecuencyFactorVector"] = [self.FrecuencyFactorVector1, self.FrecuencyFactorVector2, self.FrecuencyFactorVector3, self.FrecuencyFactorVector4]
                self.vec_objetos[2]["CombinedFactorVector"] = [self.CombinedFactorVector1, self.CombinedFactorVector2, self.CombinedFactorVector3, self.CombinedFactorVector4]

                # display the vector:
                self.window.object3Time.setText(str(np.around(self.vec_objetos[2]["timeFactorVector"], 4)))
                self.window.object3Frecuency.setText(str(np.around(self.vec_objetos[2]["FrecuencyFactorVector"], 4)))
                self.window.object3Combined.setText(str(np.around(self.vec_objetos[2]["CombinedFactorVector"], 3)))

                # flag used to determined if its moment to tran the neural network
                self.is_object3Saved = True

            # update the progress barr:
            self.training_handler()

            # save the data to the file
            if self.sensorType == MODE_T1R1:

                #create the input and output vector depending on the sensor configuration:
                x = np.array( 
                    self.vec_objetos[current_index]["timeFactorVector"][:1] + 
                    self.vec_objetos[current_index]["FrecuencyFactorVector"][:1] + 
                    self.vec_objetos[current_index]["CombinedFactorVector"][:1] 
                ,  dtype=float)

                try:
                    # save the data to hte file
                    self.neural_t1r1.save_data_file(x, self.object_Name[current_index])
                except Exception as e:
                    print(e)
                    msgBox = QtGui.QMessageBox()
                    msgBox.setText("check your sensor configuration")
                    msgBox.setWindowTitle("Ups, something went wrong training the network")
                    ret = msgBox.exec_()
                    return
            
            elif self.sensorType == MODE_T1R2:

                #create the input and output vector depending on the sensor configuration:
                x = np.array( 
                    self.vec_objetos[current_index]["timeFactorVector"][:2] + 
                    self.vec_objetos[current_index]["FrecuencyFactorVector"][:2] +
                    self.vec_objetos[current_index]["CombinedFactorVector"][:2] 
                ,  dtype=float)
                try: 
                    # save the data to hte file
                    self.neural_t1r2.save_data_file(x, self.object_Name[current_index])
                except Exception as e:
                    print(e)
                    msgBox = QtGui.QMessageBox()
                    msgBox.setText("check your sensor configuration")
                    msgBox.setWindowTitle("Ups, something went wrong training the network")
                    ret = msgBox.exec_()
                    return

            elif self.sensorType == MODE_T2R1:
                #create the input and output vector depending on the sensor configuration:
                x = np.array( 
                    self.vec_objetos[current_index]["timeFactorVector"][0] + self.vec_objetos[current_index]["timeFactorVector"][2] +  
                    self.vec_objetos[current_index]["FrecuencyFactorVector"][0] + self.vec_objetos[current_index]["FrecuencyFactorVector"][2] + 
                    self.vec_objetos[current_index]["CombinedFactorVector"][0] + self.vec_objetos[current_index]["CombinedFactorVector"][2] 
                ,  dtype=float)

                try: 
                    # save the data to hte file
                    self.neural_t2r1.save_data_file(x, self.object_Name[current_index])
                except Exception as e:
                    print(e)
                    msgBox = QtGui.QMessageBox()
                    msgBox.setText("check your sensor configuration")
                    msgBox.setWindowTitle("Ups, something went wrong training the network")
                    ret = msgBox.exec_()
                    return

            elif self.sensorType == MODE_T2R2:
                #create the input and output vector depending on the sensor configuration:
                print("object dictionary: "+ str(self.vec_objetos))

                x = np.array( 
                    self.vec_objetos[current_index]["timeFactorVector"] +
                    self.vec_objetos[current_index]["FrecuencyFactorVector"] +
                    self.vec_objetos[current_index]["CombinedFactorVector"] 
                ,  dtype=float)


                # save the data to hte file
                try:
                    self.neural_t2r2.save_data_file(x, self.object_Name[current_index])
                except Exception as e:
                    print(e)
                    msgBox = QtGui.QMessageBox()
                    msgBox.setText("check your sensor configuration")
                    msgBox.setWindowTitle("Ups, something went wrong training the network")
                    ret = msgBox.exec_()
                    return

            # you got the wrong configuration
            else:
                msgBox = QtGui.QMessageBox()
                msgBox.setText("check your sensor configuration")
                msgBox.setWindowTitle("Ups, something went wrong training the network")
                ret = msgBox.exec_()
                return

            # if all 3 objects are saved train your neural net:
            if self.num_trains3 >= self.num_trains  and self.num_trains3 >= self.num_trains and self.num_trains3 >= self.num_trains:
                
                #show the message window:
                msgBox = QtGui.QMessageBox()
                msgBox.setText("Prepare for training")
                msgBox.setWindowTitle("it might take a while")
                msgBox.setInformativeText("¿Do you want to train your system now?")
                msgBox.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.Cancel)
                msgBox.setDefaultButton(QtGui.QMessageBox.Yes)
                ret = msgBox.exec_()

                if ret == QtGui.QMessageBox.Yes:
                    self.is_neuralTrained = True

                    # train the corresponding neural network depending on the confguration:
                    if self.sensorType == MODE_T1R1:
                        actual_network = self.neural_t1r1
                        
                    elif self.sensorType == MODE_T1R2:
                        actual_network = self.neural_t1r2

                    elif self.sensorType == MODE_T2R1:
                        actual_network = self.neural_t2r1

                    elif self.sensorType == MODE_T2R2:
                        actual_network = self.neural_t2r2
                    else:
                        msgBox = QtGui.QMessageBox()
                        msgBox.setText("check your sensor configuration!!")
                        msgBox.setWindowTitle("Ups, something went wrong training the network")
                        ret = msgBox.exec_()
                        return

                    actual_network.train_neural_network()
                    
                else:
                    print("canceled")


        elif ret == QtGui.QMessageBox.Cancel:
            # cancel was clicked
            save = 0
            print("canceled pressed")       
        else:
            print("canceled")

    def get_dat(self):

        """
        #get the data:
        try:
            self.s1, self.s2, self.s3, self.s4 = get_data() # this function returns None on falure vectors
            self.num_datos = np.arange(len(self.s1))
            self.t = self.num_datos*(1/self.frec_muestreo)

        except Exception as e:
            print("error found")
            print(e)
            msgBox = QtGui.QMessageBox()
            msgBox.setText("There is a problem with your ultrasonic sensor, please check the driver or contact your software provider")
            msgBox.setWindowTitle("Ups, something went wrong")
            ret = msgBox.exec_()
        """
        
        #simulate the data
        self.s1,self.s2,self.s3,self.s4 = [None, None, None, None]

        sine_freq = 1000
        self.num_datos = 50 # 185 
        self.n = np.arange(self.num_datos)
        self.t = self.n*(1/self.frec_muestreo)

        # create vectors depending on the 
        r = random.randint(0, 2)
        if r == 0:
            self.s1 = np.sin(2 * pi * sine_freq * self.t) 
            self.s2 = cos(2 * pi * 0.5 *sine_freq * self.t) 
            self.s3 = np.sin(2 * pi * 2*sine_freq * self.t) + cos(2 * pi * sine_freq*0.1 * self.t) 
            self.s4 = np.sin(2 * pi * 2*sine_freq * self.t) + np.sin(2 * pi * sine_freq * self.t) 
        elif r == 1:
            self.s1 = np.arctan(2 * pi * 20 * sine_freq * self.t) + (np.random.rand(self.num_datos))*0.2
            self.s2 = np.arctan(2 * pi * 200 * sine_freq * self.t) + (np.random.rand(self.num_datos))/10
            self.s3 = np.arctan(2 * pi * 100 * sine_freq * self.t) + np.arctan(2 * pi * sine_freq * self.t) + (np.random.rand(self.num_datos))/100
            self.s4 = np.arctan(2 * pi * 20 * sine_freq * self.t) + np.arctan(2 * pi * sine_freq/0.3 * self.t) + (np.random.rand(self.num_datos))/20
        elif r == 2:
            self.s1 = np.tan(2 * pi * 2*sine_freq * self.t) + np.tan(2 * pi * sine_freq *0.2 * self.t) + (np.random.rand(self.num_datos))/0.1
            self.s2 = np.tan(2 * pi * 5*sine_freq * self.t) + np.tan(2 * pi * 2 * sine_freq * self.t) + (np.random.rand(self.num_datos)) *0.5
            self.s3 = np.tan(2 * pi * 6*sine_freq * self.t) + (np.random.rand(self.num_datos)) 
            self.s4 = np.tan(2 * pi * sine_freq * self.t) + (np.random.rand(self.num_datos))*0.2
        

        vecs = [self.s1, self.s2, self.s3, self.s4]
        filt_vecs = [None, None, None, None]
        
        for i in range(len(vecs)):
            print("the vectoorrr data is")
            print(vecs[i])
            # Filter requirements.
            order = 8
            cutoff = 2000  # desired cutoff frequency of the low pass filter, Hz
            multi_order = 5 # the order of the multiplication filter
            
            # Filter the output data
            filter_y = butter_lowpass_filter(vecs[i], cutoff, self.frec_muestreo, order) # filter the input data
            mult_filter = np.convolve(filter_y, np.full(multi_order, 1/multi_order), 'same')

            filt_vecs[i] = mult_filter
            print("the filtered data is")
            print(filt_vecs[i])
            
        return filt_vecs

    def capture_data_function(self):

        #get the data:
        vecs = self.get_dat()

        print("vecs fron adquisition", vecs)

        #save the characteristics on the vectors:
        signal = Extract_features()

        # Process every single enabled grup:
        if self.window.t1r1Enable.isChecked():
            
            # if the data is empty break
            if not (np.any(vecs[0]) == 1): 
                msgBox = QtGui.QMessageBox()
                msgBox.setText("please check the configuration of the t1r1 channel")
                msgBox.setWindowTitle("Ups, there is a problem with the serial data")
                ret = msgBox.exec_()                
                return
        
            #graficate response:
            self.my_plot_t1r1.update_data(self.t, vecs[0])

            # get the characteristics
            self.FrecuencyFactorVector1 = signal.frecuency_extraction(vecs[0],self.frec_muestreo)   
            self.timeFactorVector1 = signal.temporal_extraction(vecs[0],self.frec_muestreo)
            self.CombinedFactorVector1 = signal.energy_extraction(vecs[0])

            print("frecuency1 ", self.FrecuencyFactorVector1)
            print("frecuency2 ", self.timeFactorVector1)
            print("frecuency3 ", self.CombinedFactorVector1)

            #show the results of the algorithm on the current plot
            self.window.t1r1Time.display(self.timeFactorVector1)
            self.window.t1r1Frecuency.display(self.FrecuencyFactorVector1)
            self.window.t1r1Combined.display(self.CombinedFactorVector1)

        if self.window.t1r2Enable.isChecked():
            
            # if the data is empty break
            if not (np.any(vecs[1]) == 1): 
                msgBox = QtGui.QMessageBox()
                msgBox.setText("please check the configuration of the t1r2 channel")
                msgBox.setWindowTitle("Ups, there is a problem with the serial data")
                ret = msgBox.exec_()       
                return

            #graficate response:
            self.my_plot_t1r2.update_data(self.t, vecs[1])

            # get the characteristics
            self.FrecuencyFactorVector2 = signal.frecuency_extraction(vecs[1],self.frec_muestreo)   
            self.timeFactorVector2 = signal.temporal_extraction(vecs[1],self.frec_muestreo)
            self.CombinedFactorVector2 = signal.energy_extraction(vecs[1])

            #show the results of the algorithm on the current plot
            self.window.t1r2Time.display(self.timeFactorVector2)
            self.window.t1r2Frecuency.display(self.FrecuencyFactorVector2)
            self.window.t1r2Combined.display(self.CombinedFactorVector2)

        if self.window.t2r1Enable.isChecked():
            
            # if the data is empty break
            if not (np.any(vecs[2]) == 1): 
                msgBox = QtGui.QMessageBox()
                msgBox.setText("please check the configuration of the t2r1 channel")
                msgBox.setWindowTitle("Ups, there is a problem with the serial data")
                ret = msgBox.exec_()       
                return

            #graficate response:
            self.my_plot_t2r1.update_data(self.t, vecs[2])

            # get the characteristics
            self.FrecuencyFactorVector3 = signal.frecuency_extraction(vecs[2],self.frec_muestreo)   
            self.timeFactorVector3 = signal.temporal_extraction(vecs[2],self.frec_muestreo)
            self.CombinedFactorVector3 = signal.energy_extraction(vecs[2])

            #show the results of the algorithm on the current plot   
            self.window.t2r1Time.display(self.timeFactorVector3)
            self.window.t2r1Frecuency.display(self.FrecuencyFactorVector3)
            self.window.t2r1Combined.display(self.CombinedFactorVector3)

        if self.window.t2r2Enable.isChecked():
            
            # if the data is empty break
            if not (np.any(vecs[3]) == 1): 
                msgBox = QtGui.QMessageBox()
                msgBox.setText("please check the configuration of the t2r2 channel")
                msgBox.setWindowTitle("Ups, there is a problem with the serial data")
                ret = msgBox.exec_()       
                return

            #graficate response:
            self.my_plot_t2r2.update_data(self.t, vecs[3])

            # get the characteristics
            self.FrecuencyFactorVector4 = signal.frecuency_extraction(vecs[3],self.frec_muestreo)   
            self.timeFactorVector4 = signal.temporal_extraction(vecs[3],self.frec_muestreo)
            self.CombinedFactorVector4 = signal.energy_extraction(vecs[3])

            #show the results of the algorithm on the current plot
            self.window.t2r2Time.display(self.timeFactorVector4)
            self.window.t2r2Frecuency.display(self.FrecuencyFactorVector4)
            self.window.t2r2Combined.display(self.CombinedFactorVector4)
        
        print("data adquired")
        #percentaje object from jaimen
        #p_ob1,p_ob2,p_ob3,name_object = neural_network(dF,dT,E)

    def configureSensor(self, btPressed, typeAction):

        print("configuring sensor")
        print(btPressed)
        print(typeAction)

        # reset everything
        self.is_neuralTrained = False
        self.is_object1Saved = False
        self.is_object2Saved = False
        self.is_object3Saved = False
        self.num_trains1 = 0
        self.num_trains2 = 0
        self.num_trains3 = 0
        self.window.progressBar1.setValue(0)
        self.window.progressBar2.setValue(0)
        self.window.progressBar3.setValue(0)
        self.neural_t1r1.errase_data_file()
        self.neural_t1r2.errase_data_file()
        self.neural_t2r1.errase_data_file()
        self.neural_t2r2.errase_data_file()

        
        # Disable data depending on the checkbox you activate
        if btPressed == "t1r1":
            self.window.t1r1.setEnabled(self.window.t1r1Enable.isChecked())
            # Erase the display
            self.window.t1r1Time.display(0)
            self.window.t1r1Frecuency.display(0)
            self.window.t1r1Combined.display(0)
            # Empty the graph:
            self.my_plot_t1r1.update_data([0], [0])
            # Empty buffer:
            self.empty_characteristics_buffer(1)

        elif btPressed == "t1r2":
            self.window.t1r2.setEnabled(self.window.t1r2Enable.isChecked())
            # Erase the display
            self.window.t1r2Time.display(0)
            self.window.t1r2Frecuency.display(0)
            self.window.t1r2Combined.display(0)
            # Empty the graph:
            self.my_plot_t1r2.update_data([0], [0])
            # Empty buffer:
            self.empty_characteristics_buffer(2)

        elif btPressed == "t2r1":
            self.window.t2r1.setEnabled(self.window.t2r1Enable.isChecked())
            # Erase the display
            self.window.t2r1Time.display(0)
            self.window.t2r1Frecuency.display(0)
            self.window.t2r1Combined.display(0)
            #Empty the graph:
            self.my_plot_t2r1.update_data([0], [0])
            # Empty buffer:
            self.empty_characteristics_buffer(3)

        elif btPressed == "t2r2":
            self.window.t2r2.setEnabled(self.window.t2r2Enable.isChecked())
            # Erase the display
            self.window.t2r2Time.display(0)
            self.window.t2r2Frecuency.display(0)
            self.window.t2r2Combined.display(0)
            #Empty the graph:
            self.my_plot_t2r2.update_data([0], [0])
            # Empty buffer:
            self.empty_characteristics_buffer(4)
      
        # change the current sensor type mode
        if  (self.window.t1r1Enable.isChecked()) and not (
            self.window.t1r2Enable.isChecked()) and not (
            self.window.t2r1Enable.isChecked()) and not(
            self.window.t2r2Enable.isChecked()):  
            self.sensorType = MODE_T1R1

        elif (self.window.t1r1Enable.isChecked()) and (
            self.window.t1r2Enable.isChecked()) and not(
            self.window.t2r1Enable.isChecked()) and not(
            self.window.t2r2Enable.isChecked()):  
            self.sensorType = MODE_T1R2

        elif (self.window.t1r1Enable.isChecked()) and not(
            self.window.t1r2Enable.isChecked()) and (
            self.window.t2r1Enable.isChecked()) and not(
            self.window.t2r2Enable.isChecked()):  
            self.sensorType = MODE_T2R1

        elif (self.window.t1r1Enable.isChecked()) and (
            self.window.t1r2Enable.isChecked()) and (
            self.window.t2r1Enable.isChecked()) and (
            self.window.t2r2Enable.isChecked()):  
            self.sensorType = MODE_T2R2
        else:
            self.sensorType = MODE_NONE
        
        print("the sensor type is: " + str(self.sensorType))


    def train_neural_net(self):

        print("neural net being trained")
        print(self.object1_timeFactorVector)
        print(self.object1_FrecuencyFactorVector)

        # train the corresponding neural network depending on the confguration:
        if self.sensorType == MODE_T1R1:
            actual_network = self.neural_t1r1
            
        elif self.sensorType == MODE_T1R2:
            actual_network = self.neural_t1r2

        elif self.sensorType == MODE_T2R1:
            actual_network = self.neural_t2r1

        elif self.sensorType == MODE_T2R2:
            actual_network = self.neural_t2r2
        else:
            msgBox = QtGui.QMessageBox()
            msgBox.setText("check your sensor configuration")
            msgBox.setWindowTitle("Ups, something went wrong training the network")
            ret = msgBox.exec_()
            return

        actual_network.train_neural_network()

    def training_handler (self):

        self.window.progressBar1.setValue(100 * self.num_trains1/self.num_trains)
        self.window.progressBar2.setValue(100 * self.num_trains2/self.num_trains)
        self.window.progressBar3.setValue(100 * self.num_trains3/self.num_trains)

        
    def identify_fuction(self):
        
        # only identify if the neural net is trained
        if not self.is_neuralTrained: 
            msgBox = QtGui.QMessageBox()
            msgBox.setText("please program all the objects before the identification")
            msgBox.setWindowTitle("sights, train the system")
            ret = msgBox.exec_()
            return

        #get the data:
        vecs = self.get_dat()

        #create the object to extract the characteristics:
        signal = Extract_features() 

        # use neural network to predict the output depenting on the sensor type:
        if self.sensorType == MODE_T1R1:
            print("identifying for type of sensor T1R1")
            # Plot the gathered data
            try:
                self.my_plot_multi.update_data(self.t, np.array(vecs[0]))
            except Exception as e:
                print(e)
            
            # gather the vector factors
            inputData = np.array([
                signal.temporal_extraction(vecs[0],self.frec_muestreo),
                signal.frecuency_extraction(vecs[0], self.frec_muestreo), 
                signal.energy_extraction(vecs[0])
            ],  dtype=float)

            ret = self.neural_t1r1.predict_neural_network(inputData) #this is a printing function

        elif self.sensorType == MODE_T1R2:
            print("identifying for type of sensor T1R2")
            # Plot the gathered data
            try:
                self.my_plot_multi.update_data(self.t, np.array(vecs[:2]))
            except Exception as e:
                print(e)
            
            # gather the vector factors
            inputData = np.array([
                signal.temporal_extraction(vecs[0],self.frec_muestreo),
                signal.temporal_extraction(vecs[1],self.frec_muestreo),

                signal.frecuency_extraction(vecs[0], self.frec_muestreo), 
                signal.frecuency_extraction(vecs[1], self.frec_muestreo), 

                signal.energy_extraction(vecs[0]),
                signal.energy_extraction(vecs[1])
            ],  dtype=float)
            relative_max = np.amax(inputData, axis=0) # gives the max of each characteristics (compared to the other object)
            
            ret = self.neural_t1r2.predict_neural_network(inputData) # get the output of the neural net

        elif self.sensorType == MODE_T2R1:
            print("identifying for type of sensor T2R1")
            # Plot the gathered data
            try:
                self.my_plot_multi.update_data(self.t, np.array([vecs[0], vecs[2]]) )
            except Exception as e:
                print(e)
            # gather the vector factors
            inputData = np.array([
                signal.temporal_extraction(vecs[0],self.frec_muestreo),
                signal.temporal_extraction(vecs[2],self.frec_muestreo),
                signal.frecuency_extraction(vecs[0], self.frec_muestreo), 
                signal.frecuency_extraction(vecs[2], self.frec_muestreo),
                signal.energy_extraction(vecs[0]),
                signal.energy_extraction(vecs[2])
            ],  dtype=float)

            ret = self.neural_t2r1.predict_neural_network(inputData) # get the output of the neural net

        elif self.sensorType == MODE_T2R2:
            print("identifying for type of sensor T2R2")
            # Plot the gathered data
            try:
                self.my_plot_multi.update_data(self.t, np.array(vecs))
            except Exception as e:
                print(e)
            
            # gather the vector factors
            inputData = np.array([

                signal.temporal_extraction(vecs[0],self.frec_muestreo),
                signal.temporal_extraction(vecs[1],self.frec_muestreo),
                signal.temporal_extraction(vecs[2],self.frec_muestreo),
                signal.temporal_extraction(vecs[3],self.frec_muestreo),
                signal.frecuency_extraction(vecs[0], self.frec_muestreo), 
                signal.frecuency_extraction(vecs[1], self.frec_muestreo), 
                signal.frecuency_extraction(vecs[2], self.frec_muestreo), 
                signal.frecuency_extraction(vecs[3], self.frec_muestreo), 
                signal.energy_extraction(vecs[0]),
                signal.energy_extraction(vecs[1]),
                signal.energy_extraction(vecs[2]),
                signal.energy_extraction(vecs[3])

            ],  dtype=float)
            relative_max = np.amax(inputData, axis=0) # gives the max of each characteristics (compared to the other object)
            ret = self.neural_t2r2.predict_neural_network(inputData) # get the output of the neural net
        else:
            msgBox = QtGui.QMessageBox()
            msgBox.setText("check your sensor configuration")
            msgBox.setWindowTitle("Ups, something went wrong")
            ret = msgBox.exec_()
            return
        
        print(ret[0])
        self.window.object1_result.display(100 * ret[0]) # obj1
        self.window.object2_result.display(100 * ret[1]) # obj2
        self.window.object3_result.display(100 * ret[2]) # obj3

        tolerance = 0.6 # 50 %

        # check the minimun tolerance
        if ret[0] > tolerance or ret[1] > tolerance or ret[2] > tolerance:
            self.window.objectName_result.setText(ret[3]) # display the saved name
        # display none
        else:
            self.window.objectName_result.setText("None")


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

        self.myPlot = self.addPlot()
        #self.myPlot.setLabels(left='Valor')
        self.myPlot.setLabels(bottom='tiempo')

        self.newLine = self.myPlot.plot(pen = {'color': (0, 85, 127), 'width': 2} )

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

        self.a = []
        self.b = []
        self.c = []
        self.d = []

        #self.traces = dict()
        #self.timer = pg.QtCore.QTimer()
        #self.timer.timeout.connect(self.update_data)

        # to add this widget to the widget parent:
        layout = pg.QtGui.QVBoxLayout()
        widget.setLayout(layout)
        # self.setParent(widget)
        layout.addWidget(self)

        self.myPlot = self.addPlot(title = graphName)
        #self.myPlot.setLabels(left='Valor')
        self.myPlot.setLabels(bottom='tiempo')

        self.traceT1R1 = self.myPlot.plot(pen = {'color': (255,115,117), 'width': 2} )
        self.traceT1R2 = self.myPlot.plot(pen = {'color': (58, 117,225), 'width': 2} )
        self.traceT2R1 = self.myPlot.plot(pen = {'color': (255, 255 , 116), 'width': 2} )
        self.traceT2R2 = self.myPlot.plot(pen = {'color': (243, 255, 213), 'width': 2} )


    def update_data(self, dataset_x, datasets_y):
        self.traceT1R1.setData(dataset_x, datasets_y[0])
        self.traceT1R2.setData(dataset_x, datasets_y[1])
        self.traceT2R1.setData(dataset_x, datasets_y[2])
        self.traceT2R2.setData(dataset_x, datasets_y[3])