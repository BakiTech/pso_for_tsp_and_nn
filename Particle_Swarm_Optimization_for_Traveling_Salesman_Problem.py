import random
import math

class Graph( ):
    data = {}
    
    def __init__( self, data):
        self.data = data
        
    def dist( self, node1, node2):
        if node1 == node2:
            return 0
        try:
            return self.data[ node1][ node2]
        except:
            return math.inf
    
    def neignbors_of( self, node):
        return self.data[ node]
    
    def nodes( self):
        nodes = []
        for i in range( len( self.data)):
            nodes.append( i)
        return nodes
    
    def number_of_nodes( self):
        return len( self.data)
    
class Particle:
    
    def __init__( self, graph: Graph, problem):
        self.problem= problem #-1 for min & +1 for max
        self.graph= graph
        self.route= []
        self.local_best_route= []
        if problem == -1:
            self.fitness_local_best_route= float( "inf")
            self.fitness_route= float( "inf")
        if problem == 1:
            self.fitness_local_best_route= -float( "inf")
            self.fitness_route= -float( "inf")
        
        for i in range( self.graph.number_of_nodes()):
            self.route.append( i+1)
        random.shuffle( self.route)
        
        
    def cost( self):
        cost = 0
        for i in range( len( self.route)):
            node1 = self.route[ i]
            if i == len( self.route)-1:
                node2 = self.route[ 0]
            else:
                node2 = self.route[ i+1]
            cost += self.graph.dist( node1-1, node2-1)
        return cost
        
    def evaluate( self):
        self.fitness_route = self.cost()
        if self.problem == -1:
            if self.fitness_route < self.fitness_local_best_route:
                self.local_best_route =self.route
                self.fitness_local_best_route = self.fitness_route
        if self.problem == 1:
            if self.fitness_route > self.fitness_local_best_route:
                self.local_best_route =self.route
                self.fitness_local_best_route = self.fitness_route
                
    def get_mask( self, x):
        mask = []
        for i in range( self.graph.number_of_nodes()):
            if x%2 == 1:
                mask.append( True)
            else:
                mask.append( False)
            x = int( x/2)
        mask.reverse()
        return mask
                
    def update_mask( self, w, c1, c2):
        r1 = random.randrange( 0, 2**self.graph.number_of_nodes())
        r2 = random.randrange( 0, 2**self.graph.number_of_nodes())
        r = random.randrange( 0, 2**self.graph.number_of_nodes())

        self.cognitive_mask = self.get_mask( (r1 * c1) % (2**self.graph.number_of_nodes() +1))
        self.social_mask = self.get_mask( (r2* c2) % (2**self.graph.number_of_nodes() +1))
        self.current_mask = self.get_mask( (r* w) % (2**self.graph.number_of_nodes() +1))
        
    def update_route( self, global_best_route):
        new_route = []
        for i in range( self.graph.number_of_nodes()):
            if self.current_mask[ i]:
                new_route.append( self.route[ i])
        for i in range( self.graph.number_of_nodes()):
            if self.cognitive_mask[ i] and not self.local_best_route == [] and not new_route.__contains__( self.local_best_route[ i]):
                new_route.append( self.local_best_route[ i])
        for i in range( self.graph.number_of_nodes()):
            if self.social_mask[ i] and not global_best_route == [] and not new_route.__contains__( global_best_route[ i]):
                new_route.append( global_best_route[ i])
                
        for i in range( self.graph.number_of_nodes()):
            if not new_route.__contains__( self.route[ i]):
                new_route.append( self.route[ i])
                
                
def solve_TSP( graph: Graph, particles_number, problem, w, c1, c2, iterations_number):
    if problem == -1:
        fitness_global_best_route = float( "inf")
    if problem == 1:
        fitness_global_best_route = -float( "inf")
    global_best_route = []
    swarm= []

    for i in range( particles_number):
        swarm.append( Particle( graph, problem))
    A = []
        
    for i in range( iterations_number):
        for j in range( particles_number):
            swarm[ j].evaluate()
            if problem == -1:
                if swarm[ j].fitness_route < fitness_global_best_route:
                    global_best_route = list( swarm[ j].route)
                    fitness_global_best_route = float( swarm[ j].fitness_route)
            if problem == 1:
                if swarm[ j].fitness_route > fitness_global_best_route:
                    global_best_route = list( swarm[ j].route)
                    fitness_global_best_route = float( swarm[ j].fitness_route)
                    
        for j in range( particles_number):
            swarm[ j].update_mask( w, c1, c2)
            swarm[ j].update_route( global_best_route)
        A.append( fitness_global_best_route)
        
    return global_best_route, fitness_global_best_route

my_graph_data = [[0, 10, 15, 20],
                   [10, 0, 35, 25],
                   [15, 35, 0, 30],
                   [20, 25, 30, 0]]
my_graph_data1 = [[0, 10, 15, 20],
                   [5, 0, 9, 10],
                   [6, 13, 0, 12],
                   [8, 8, 9, 0]]
graph_example1 = Graph( my_graph_data)

import networkx as nx 
G = nx.Graph() 

for i in range( len( my_graph_data)): 
    for j in range( len( my_graph_data)):
        if my_graph_data1[i][j] > 0 and j>i:
            G.add_edge( i+1, j+1, weight= my_graph_data[i][j]) 
      
import matplotlib.pyplot as plt 
pos=nx.spring_layout(G)
ax = plt.gca()
best_route = solve_TSP( graph_example1, 50, -1, 0.75, 0.8, 0.9, 100)
ax.set_title('Best Route: '+ str( best_route[0]) +"\n Cost: " + str( best_route[1]))
nx.draw_networkx(G,pos, with_labels=True, node_size=1500, ax=ax)
nx.draw_networkx_edge_labels(G,pos,
    edge_labels=nx.get_edge_attributes(G, 'weight'))
plt.show()

print( solve_TSP( graph_example1,
                 50, -1,
                 0.75, 0.8, 0.9,
                 100))
