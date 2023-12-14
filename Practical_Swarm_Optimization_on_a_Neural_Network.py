import numpy as np
import random

def sigmoid( x):
    return 1 / ( 1+ np.exp( - x))

def softmax( x):
    return np.exp( x) / sum( np.exp( x))


def ReLU( x):
    return np.maximum( 0, x)

class Particle:
    
    def __init__( self, sizes):
        self.fitness_local_best= 0
        self.fitness= 0
        
        self.input_layer_size= sizes[ 0]
        self.hidden_layer_size= sizes[ 1]
        self.output_layer_size= sizes[ 2]
        
        self.W1= np.random.randn( self.hidden_layer_size, self.input_layer_size)
        self.W2= np.random.randn( self.output_layer_size, self.hidden_layer_size)
        self.local_best_W1 = self.W1
        self.local_best_W2 = self.W2

            
            
    def evaluate( self, X, test_list):
        values = X.split(',')
        inputs = ( np.asfarray(values[1:]) / 255.0 * 0.99) + 0.01
        targets = np.zeros(10) + 0.01
        targets[ int(values[0])] = 0.99
        
        self.forward_pass( inputs, targets)
        self.fitness = self.accuracy( test_list)
        
        if self.fitness > self.fitness_local_best:
            self.fitness_local_best = self.fitness
            self.local_best_W1 = self.W1
            self.local_best_W2 = self.W2
            
            
    def forward_pass( self, inputs, targets):
        self.A0= inputs
        
        self.Z1= np.dot( self.W1, self.A0)
        self.A1= sigmoid( self.Z1)
        
        self.Z2= np.dot( self.W2, self.A1)
        self.A2= softmax( self.Z2)
  
        return
    
    def update_weights( self, global_best_W1, global_best_W2, w, c1, c2):
        r1_W1 = np.random.random()
        r2_W1 = np.random.random()
                                  
        r1_W2 = np.random.random()
        r2_W2 = np.random.random()
                                  
        velocity_W1 = ( w* self.W1 +
                        c1* r1_W1 * ( self.local_best_W1 - self.W1) +
                        c2* r2_W2 * ( global_best_W1 - self.W1)
                    )
        
        velocity_W2 = ( w* self.W2 +
                        c1* r1_W2 * ( self.local_best_W2 - self.W2) +
                        c2* r2_W2 * ( global_best_W2 - self.W2)
                    )
        
        self.W1 = self.W1 + velocity_W1
        self.W2 = self.W2 + velocity_W2

    def predict( self, X):
        values = X.split(',')
        inputs = ( np.asfarray( values[ 1: ]) / 255.0 * 0.99) + 0.01
        targets = np.zeros( 10) + 0.01
        targets[ int(values[0])] = 0.99
        
        self.A0= inputs
        
        self.Z1= np.dot( self.W1, self.A0)
        self.A1= sigmoid( self.Z1)
        
        self.Z2= np.dot( self.W2, self.A1)
        self.A2= softmax( self.Z2)

        prediction = np.argmax( self.Z2)
        return prediction == np.argmax( targets)
        
    def accuracy( self, data):
        predictions = []
        for X in data:
            predictions.append( self.predict( X))
        return np.mean(predictions)
        
            
        

class Neural_Network:
    def __init__( self, sizes, epochs, learning_rate, particles_number):
        self.input_layer_size= sizes[ 0]
        self.hidden_layer_size= sizes[ 1]
        self.output_layer_size= sizes[ 2]
        
        self.epochs= epochs
        self.learning_rate= learning_rate
        self.particles_number= particles_number
        
        self.swarm = []
        
        for i in range( particles_number):
            self.swarm.append( Particle( sizes))
        
        self.fitness_global_best = 0
        self.best_particle = self.swarm[ 0]
        self.global_best_W1 = self.swarm[ 0].W1
        self.global_best_W2 = self.swarm[ 0].W2

    def train( self, train_list, test_list, w, c1, c2):
        A = []
        best_particle : Particle
        
        for i in range( self.epochs):
            np.random.shuffle( train_list)
            for X in train_list:
                swarm = self.swarm
                for j in range( self.particles_number):
                    swarm[ j].evaluate( X, test_list)
                    if  swarm[ j].fitness > self.fitness_global_best:
                        self.fitness_global_best = swarm[ j].fitness
                        self.global_best_W1 = swarm[ j].W1.copy()
                        self.global_best_W2 = swarm[ j].W2.copy()
                        
                for j in range( self.particles_number):
                    swarm[ j].update_weights( self.global_best_W1, self.global_best_W2, w, c1, c2)
                A.append( self.fitness_global_best)
                
                print( "accuracy: ",  self.fitness_global_best)
            
            print( "epoch: ", i+1," accuracy: ", self.fitness_global_best )
        
        return self.fitness_global_best
    
    
train_file = open("mnist_train.csv", 'r')
test_file = open("mnist_test.csv", 'r')
train_list = train_file.readlines()
test_list = test_file.readlines()

train_file.close()
test_file.close()

reseau = Neural_Network(sizes=[784, 200, 10], epochs=10, learning_rate=0.001, particles_number=10)
reseau.train(train_list, test_list, 0.75, 0.8, 0.9)
                