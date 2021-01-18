import numpy as np
import math
import random

#SETTING HYPERPARAMETERS
learning_rate = 0.25
epochs = 30
batch_size = 10

#FUNCTIONS
def sigmoid(x):
    return 1/(1+math.exp(-x))

def logit(x):
    return math.log(x/(1-x))

def sigmoid_prime(x):
    return sigmoid(x)*(1-sigmoid(x))

def product_matrix(a, b):
    a = np.array(a)
    b = np.array(b)
    matrix = []
    for i in a:
        matrix.append(i*b)
    return np.array(matrix)

#CREATING NETWORK OBJECT CLASS
class Network:
    def __init__(self, shape):
        self.shape = shape
    
        #CREATING BIASES ARRAY
        self.biases = []
        for i in self.shape[1:]:
            self.biases.append(np.random.randn(i))
        
        #CREATING WEIGHTS ARRAY
        self.weights = []
        for i in range(0, len(self.shape)-1):
            self.weights.append(np.random.randn(shape[i]*shape[i+1])
            .reshape((shape[i+1], shape[i])))
    
    #FEEDFORWARD METHOD FOR COMPUTING NETWORK'S OUTPUT      
    def feedforward(self, activations):
        for i in range(0, len(self.shape)-1):
            activations = self.weights[i].dot(activations) + self.biases[i]
            activations = np.vectorize(sigmoid)(activations)
        return activations
    
    #OUTPUT WITH SIGMOID NOT APPLIED
    def feedforward_raw(self, activations):
        for i in range(0, len(self.shape)-2):
            activations = self.weights[i].dot(activations) + self.biases[i]
            activations = np.vectorize(sigmoid)(activations)
        activations = self.weights[len(self.shape)-2].dot(activations) + self.biases[len(self.shape)-2]
        return activations
    
    #WEIGHTED SUM FOR ANY LAYER
    def weighted_sum(self, activations, layer):
        if layer == 1:
            return activations
        else:
            for i in range(0, layer-2):
                activations = self.weights[i].dot(activations) + self.biases[i]
                activations = np.vectorize(sigmoid)(activations)
            return self.weights[layer-2].dot(activations) + self.biases[layer-2]
        
    #COST FUNCTION
    def mse(self, activations, target):
        x = self.feedforward(activations) - target
        return x.dot(x)/2
    
    #UPDATING WEIGHTS AND BIASES
    def SGD(self, activations_batch, target_batch, batch_size):
        #CREATING ZERO-ARRAYS FOR STORING TOTAL GRADIENT
        tot_b_gradient = np.array(self.biases)
        tot_w_gradient = np.array(self.weights)
        for i in range(0, len(tot_b_gradient)):
            tot_b_gradient[i] = np.zeros_like(tot_b_gradient[i])
            tot_w_gradient[i] = np.zeros_like(tot_w_gradient[i])
        
        #LOOPING OVER ITEMS IN BATCH
        for activations, target in zip(activations_batch, target_batch):
            #CALCULATING ERRORS FOR LAST LAYER
            errors = [np.multiply((self.feedforward(activations) - target),
            np.vectorize(sigmoid_prime)(self.feedforward_raw(activations)))]
            
            #ERROR FOR REMAINING LAYERS, STORING ALL IN ARRAY
            for i in range(1,len(self.shape)-1):
                #COMPUTING COMPONENTS
                t_weights = np.transpose(self.weights[-i])
                p_errors = errors[0]
                spw_sum = np.vectorize(sigmoid_prime)(
                        self.weighted_sum(activations, len(self.shape)-i))
                n_error = np.multiply(t_weights.dot(p_errors), spw_sum)
                #INSERTING ERROR FOR NEW LAYER INTO ARRAY
                errors.insert(0, n_error)
            
            #COMPUTING GRADIENT
            b_gradient = errors
            w_gradient = []
            for i in range(0, len(self.shape)-1):
                w_gradient.append(product_matrix(errors[i], self.weighted_sum(
                        activations, i+1)))
            
            #ADDING GRADIENT TO BATCH TOTAL
            for i in range(0, len(tot_b_gradient)):
                tot_b_gradient[i] = tot_b_gradient[i] + b_gradient[i]/batch_size
                tot_w_gradient[i] = tot_w_gradient[i] + w_gradient[i]/batch_size
        
        #UPDATING PARAMETERS
        for i in range(0, len(self.shape)-1):
            self.biases[i] = ((-1)*learning_rate*tot_b_gradient[i]) + self.biases[i]
            self.weights[i] = ((-1)*learning_rate*tot_w_gradient[i]) + self.weights[i]
        
                          







#--------------USING NET FOR DIGIT RECOGNITION----------------

#IMPORTING MNIST
from keras.datasets import mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

#FUNCTIONS
def v_to_d(vector):
    return list(vector).index(max(vector))

def d_to_v(digit):
    vector = np.zeros(10)
    vector[digit] = 1
    return np.array(vector)

def flatten(array):
    l = []
    for sub_array in array:
        for i in sub_array:
            l.append(i)
    return np.array(l)

def unison_shuffled_copies(a, b):
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p], b[p]


#PREPROCESSING  
#TRAINING DATASET
inputs_train = []
targets_train = []
for i in range(len(x_train)):
    inputs_train.append(flatten(x_train[i])/255)
    targets_train.append(d_to_v(y_train[i]))

#TESTING DATASET
inputs_test = []
for i in range(len(x_test)):
    inputs_test.append(flatten(x_test[i])/255)
targets_test = np.array(y_test)
inputs_test = np.array(inputs_test)



#TRAINING & TESTING
net = Network([784,100,100,10])

#TESTING BEFORE TRAINING
correct = 0
print("BEFORE TRAINING: ")
for i, j in zip (inputs_test, targets_test):
    if v_to_d(net.feedforward(i)) == j:
        correct += 1
print("Accuracy =", correct, "out of 10,000")
print(" ")
        
  
#REPEATING PROCEDURE FOR SEVERAL EPOCHS

for j in range(epochs):
    print("Epoch",j+1, "out of",epochs)

    #SINGLE-EPOCH RUN 
    #TRAINING ON TRAINING DATASET
    for i in range(0,len(inputs_train),batch_size):
        net.SGD(inputs_train[i:i+batch_size],
                targets_train[i:i+batch_size],
                batch_size)
    
    #SHUFFLING DATA AROUND
    shuffled_data = unison_shuffled_copies(np.array(inputs_train),
                                           np.array(targets_train))
    inputs_train = shuffled_data[0]
    targets_train = shuffled_data[1]
    
    #RETURNING TEST ACCURACY AFTER EPOCH
    correct = 0
    for i, j in zip (inputs_test, targets_test):
        if v_to_d(net.feedforward(i)) == j:
            correct += 1
    print("Accuracy =", correct, "out of 10,000")
    print(" ")
            


















            
        
        

