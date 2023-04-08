import copy
import numpy as np
import random as ran
from copy import deepcopy


def relu(input):
    return (np.abs(input) + input )/2



def forward(inputs, weights, bias, activation):
    if not activation == None:
        return activation(np.dot(inputs, weights) + bias)
    else:
        return np.dot(inputs, weights) + bias



def ran_num(range):
    return ran.random()*range*2 - range



class NeuralNet:

    def __init__(self,bias_range,weight_range,layers) -> None:
        self.weights = [np.array([[ran_num(weight_range) for _ in range(layers[i+1])] for n in range(layers[i])]) for i in range(len(layers[:-1]))]
        self.bias = [np.array([ran_num(bias_range) for _ in range(i)]) for i in layers[1:]]
        self.neurons = [np.array([0.0 for _ in range(i)]) for i in layers]
        self.layers = layers
    

    def big_brain(self,inputs):
        if not type(inputs) == np.array:
            self.neurons[0] = np.array(inputs)
        else:
            self.neurons[0] = inputs
        
        for n in range(len(self.neurons)):
            if n == len(self.neurons)-1:
                return self.neurons[n]
            elif n == len(self.neurons)-2:
                self.neurons[n+1] = forward(self.neurons[n],self.weights[n],self.bias[n],None)
            else:
                self.neurons[n+1] = forward(self.neurons[n],self.weights[n],self.bias[n],relu)
    

    def mutate(self,bias_range,weight_range):
        new_net = deepcopy(self)

        new_net.weights = [np.array([[new_net.weights[i][n][k] + ran_num(weight_range) for k in range(self.layers[i+1])] for n in range(self.layers[i])]) for i in range(len(self.layers[:-1]))]
        new_net.bias = [np.array([new_net.bias[n][k] + ran_num(bias_range) for k in range(self.layers[1:][n])]) for n in range(len(self.layers[1:]))]


        return new_net