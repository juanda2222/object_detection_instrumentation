

import numpy as np


class Neural_Network(object):
    def __init__(self):
        
        #parameters
        self.inputSize = 2
        self.hiddenSize = 3
        self.outputSize = 1

        #weights
        self.W1 = np.random.randn(self.inputSize, self.hiddenSize)  # (3x2) weight matrix from input to hidden layer
        self.W2 = np.random.randn(self.hiddenSize, self.outputSize)  # (3x1) weight matrix from hidden to output layer

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

    def saveWeights(self):
        np.savetxt("w1.txt", self.W1, fmt="%s")
        np.savetxt("w2.txt", self.W2, fmt="%s")

    def predict(self):
        print("Predicted data based on trained weights: ")
        print("Input (scaled): \n" + str(xPredicted))
        print("Output: \n" + str(self.forward(xPredicted)))


# x = (hours studying, hours sleeping), y = score on test, xPredicted = 4 hours studying & 8 hours sleeping (input data for prediction)
x = np.array(([2, 9], [1, 5], [3, 6]), dtype=float)
y = np.array(([10], [100], [1]), dtype=float)

xPredicted = np.array(([4, 8]), dtype=float)

# scale units
x = x / np.amax(x, axis=0)  # normalize x data using maximum of its axis (axis cero means the )
xPredicted = xPredicted / np.amax(xPredicted, axis=0)  # maximum of xPredicted (our input data for the prediction)

y = y / 100  # max test score is 100


NN = Neural_Network()

for i in range(1000):  # trains the NN 1,000 times
    print(" #" + str(i) + "\n")
    print("Input (scaled): \n" + str(x))
    print("Actual Output: \n" + str(y))
    print("Predicted Output: \n" + str(NN.forward(x)))
    print("Loss: \n" + str(np.mean(np.square(y - NN.forward(x)))))  # mean sum squared loss
    print("\n")
    NN.train(x, y)

NN.saveWeights()
NN.predict()

