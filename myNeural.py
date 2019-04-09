

import numpy as np



class Neural_Network(object):
    def __init__(self, name = "myNeural",  vector_size = 2, num_characteristics = 3, num_objects = 3):

        #parameters (just 1 hidden size)
        self.name = name
        self.inputSize = vector_size * num_characteristics
        self.hiddenSize = 10 #this is the medium space between the  input layer and the output
        self.outputSize = num_objects

        #weights
        self.W1 = np.random.randn(self.inputSize, self.hiddenSize)  # weight matrix from input to hidden layer
        self.W2 = np.random.randn(self.hiddenSize, self.outputSize)  # weight matrix from hidden to output layer

    def forward(self, x):
        #forward propagation through our network
        
        #first Layer:
        self.z = np.dot(x, self.W1)  # dot product of x (input) and first set of 3x2 weights
        self.z2 = self.sigmoid(self.z)  # activation function

        #second layer:
        self.z3 = np.dot(self.z2, self.W2)  # dot product of hidden layer (z2) and second set of 3x1 weights
        o = self.sigmoid(self.z3)  # final activation function

        return o

    def sigmoid(self, s):
        # activation function
        return 1 / (1 + np.exp(-s))

    def sigmoidPrime(self, s):
        #derivative of sigmoid
        return s * (1 - s)

    def backward(self, x, y, o):
        # backward propgate through the network
        self.o_error = y - o  # error in output
        self.o_delta = self.o_error * self.sigmoidPrime(o) # applying derivative of sigmoid to error
        self.z2_error = np.dot(self.o_delta, self.W2.T)  # z2 error: how much our hidden layer weights contributed to output error
        self.z2_delta = self.z2_error * self.sigmoidPrime(self.z2)  # applying derivative of sigmoid to z2 error
        
        self.W2 += np.dot(self.z2.T, self.o_delta)  # adjusting second set (hidden --> output) weights
        self.W1 += np.dot(x.T, self.z2_delta)  # adjusting first set (input --> hidden) weights
        

    def train(self, x, y):
        o = self.forward(x)
        self.backward(x, y, o)
    
    def train_nTimes(self, x, y, num_trains = 100000, noise_percentage = 0.05, funcPer=None):
        print("number of trains "+ str(num_trains))
        print("training started...")
        for i in range(num_trains): 
            # train 1 timex
            self.train(x + np.random.rand(self.outputSize, self.inputSize) * noise_percentage, y)
            # detects the percentage of the training
            if i == int(num_trains*0.10): 
                funcPer(10)
            elif i == int(num_trains*0.20): 
                funcPer(20)
            elif i == int(num_trains*0.30): 
                funcPer(30)
            elif i == int(num_trains*0.40): 
                funcPer(40)
            elif i == int(num_trains*0.50): 
                funcPer(50)
            elif i == int(num_trains*0.60): 
                funcPer(60)
            elif i == int(num_trains*0.7): 
                funcPer(70)
            elif i == int(num_trains*0.8): 
                funcPer(80)
            elif i == int(num_trains*0.9): 
                funcPer(90)
        print("training finished...")
        funcPer(100)

    def saveWeights(self):  
        np.savetxt(self.name+"_w1.txt", self.W1, fmt="%s")
        np.savetxt(self.name+"_w2.txt", self.W2, fmt="%s")

    def predict(self, dif_input):
        print("Predicted data based on trained weights: ")
        print("Input (scaled): \n" + str(dif_input))
        print("Output: \n" + str(self.forward(dif_input)))

if __name__ == "__main__":

    """
    #create the data for the neural network
    # group of input dataset [tf1, tf2, tf3, tf4, ff1, ff2, ff3, ff4, cf1, cf2, cf3, cf4 ]
    x = np.array(([2, 9, 3, 6, 1, 1, 1, 5, 8, 2, 3, 6,], [1, 9, 4, 6, 0, 1, 4, 5, 5, 1, 0, 5,], [0, 5, 4, 6, 4, 1, 4, 9, 5, 0, 0, 10,]), dtype=float)
    # group of output dataset [obj1, obj2, obj3]
    y = np.array(([1, 0, 0], [0, 1, 0], [0, 0, 1]), dtype=float)

    # predict this new set of data taken from the 1st object
    xPredicted = np.array(([2, 9, 3, 6, 1, 10, 3, 5, 8, 2, 3, 6,]), dtype=float)
    """

    #create the data for the neural network
    # group of input dataset [tf1, tf2, tf3, tf4, ff1, ff2, ff3, ff4, cf1, cf2, cf3, cf4 ]
    x = np.array(([2, 9, 1, 1, 8, 2], [1, 9, 0, 1, 5, 1 ], [0, 5, 4, 1, 5, 0]), dtype=float)
    # group of output dataset [obj1, obj2, obj3]
    y = np.array(([1, 0, 0], [0, 1, 0], [0, 0, 1]), dtype=float)
    # predict this new set of data taken from the 1st object
    xPredicted = np.array(([2, 9, 1, 10, 8, 2,]), dtype=float)

    # scale units
    absolute_max = np.amax(x) # gives the max value of all the values on the matrix
    relative_max = np.amax(x, axis=0) # gives the max of each characteristics (compared to the other object)
    x = x / absolute_max  # normalize x data using maximum of its axis (axis cero means the )
    xPredicted = xPredicted / absolute_max  # maximum of xPredicted (our input data for the prediction)

    NN = Neural_Network()
    NN.train_nTimes(x, y, 100000, 0.20)
    NN.saveWeights()

    print("Input (scaled): \n" + str(x))
    print("Actual Output: \n" + str(y))
    print("Predicted Output: \n" + str(NN.forward(x)))  
    print("Loss: \n" + str(np.mean(np.square(y - NN.forward(x)))))

    NN.predict(xPredicted)

