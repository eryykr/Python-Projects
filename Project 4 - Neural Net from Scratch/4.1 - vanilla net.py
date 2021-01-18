import numpy as np
import math
import random

#SETTING HYPERPARAMETERS
learning_rate = 0.5
epochs = 20
batch_size = 20

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
        for i in range(len(self.shape)-1):
            self.weights.append(np.random.randn(shape[i]*shape[i+1])
            .reshape((shape[i+1], shape[i])))
    
    #FEEDFORWARD METHOD FOR COMPUTING NETWORK'S OUTPUT      
    def feedforward(self, activations):
        for i in range(len(self.shape)-1):
            activations = self.weights[i].dot(activations) + self.biases[i]
            activations = np.vectorize(sigmoid)(activations)
        return activations
    
    #OUTPUT WITH SIGMOID NOT APPLIED
    def feedforward_raw(self, activations):
        return np.vectorize(logit)(self.feedforward(activations))
    
    #WEIGHTED SUM FOR ANY LAYER
    def weighted_sum(self, activations, layer):
        if layer == 1:
            return activations
        else:
            for i in range(layer-2):
                activations = self.weights[i].dot(activations) + self.biases[i]
                activations = np.vectorize(sigmoid)(activations)
            return self.weights[layer-2].dot(activations) + self.biases[layer-2]
        
    #COST FUNCTION
    def mse(self, activations, target):
        x = self.feedforward(activations) - target
        return x.dot(x)/2
    
    #UPDATING WEIGHTS AND BIASES
    def gradient_descent(self, activations, target):
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
        for i in range(len(self.shape)-1):
            w_gradient.append(product_matrix(errors[i], self.weighted_sum(
                    activations, i+1)))
        #UPDATING PARAMETERS
        for i in range(len(self.shape)-1):
            self.biases[i] = ((-1)*learning_rate*b_gradient[i]) + self.biases[i]
            self.weights[i] = ((-1)*learning_rate*w_gradient[i]) + self.weights[i]
        
                           

#-----TESTING ON ARTIFICIAL DATA (training net to return the input)-----
nn = Network([5,10,5])

#CREATING TRAINING DATA
data = []
for i in range(10000):
    inpt = np.zeros(5)
    inpt[random.randint(0,4)] = 1
    data.append(inpt)

#TRAINING
for i in data:
    nn.gradient_descent(i, i)
print("Epoch Complete")
  
#CHECKING  
print(nn.feedforward([0,1,0,0,0]))

print(nn.weights)


        
            
            
        
        

