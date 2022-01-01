import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.shortest_paths.weighted import dijkstra_path
import numpy as np
import math

Gr = nx.Graph()


class Algorithm:
    def __init__(self, G, pos, start_name, destination_name, index_name):
        """ Graph data"""
        self.G = G
        self.pos = pos
        self.len = len(G)
        self.s_name = start_name
        self.d_name = destination_name
        self.i_name = index_name

        """ Agent data"""
        self.N_sda = 3  # number of sda
        self.N_ss = self.len  # number of smell spots
        self.N_nd = 2  # the number of who can each the destination
        self.a = 100  # init smell values
        self.b = 10  # Decrease Constant
        self.r = self.distance()
 

        self.Agent = []
        for i in range(self.N_sda):
            self.Agent += [[self.s_name, 0]]  # [Current position, Total]

        self.SmellSpot = []
        for i in range(self.N_ss):
            ### diciding smell value###
            
            # smell_value = self.a  / self.r[i] # actual smell of the position ..... when the value is zero, this is can't be calculated 
            smell_value = 1 / (self.a + self.b * self.r[i] )
            print(smell_value)
            
            self.SmellSpot += [[self.i_name[i], "none", smell_value]]  # [name of node, Reached agent, Smell value]
            

        # init
        self.goal = 0
        self.SmellSpot[self.i_name.index(self.s_name)][1] = "init"

        """ Action """
        self.action()
        
        for i in range(len(self.Agent)):
             if self.Agent[i][1] == 0:
                 self.Agent[i][1] = math.inf
        
        
        """ result """
        self.dijkstra_score = self.dijkstra(self.s_name, self.d_name)
        self.sda_score = self.result() 

    def dijkstra(self, a, b):
        score = nx.dijkstra_path_length(self.G, a, b)
        
        # """
        print("================================")
        print("Dijkstra Answer")
        print(nx.dijkstra_path(self.G, a, b))
        print("length: %f" % score)
        print("================================")
        # """
        return score

    def plot(self):
        nx.draw(self.G, self.pos, with_labels=True)
        plt.show()

    def distance(self):
        distance = []
        x = self.pos[self.d_name][0]  # destination
        y = self.pos[self.d_name][1]  # destination

        for i in self.i_name:
            distance += [np.sqrt((self.pos[i][0] - x) ** 2 + (self.pos[i][1] - y) ** 2)]

        return distance

    def action(self):
        for i in range(self.N_sda):
            print("Agent %d" % i) #VIS

            if self.goal < self.N_nd:
                while self.Agent[i][0] != self.d_name:
                    next_position = self.check_around(self.Agent[i][0])
                    if next_position == "stop":
                        """
                        if it mightn't reach to d_name(goal), the data is saved.
                        so it have to input numver such as infinity( as far as big) to the data coudn't reach to d_name(goal).
                        """
                        self.Agent[i][1] += math.inf
                        break
                    else:
                        self.move(next_position, i)
                        print(self.Agent[i]) #VIS

                if self.Agent[i][0] == self.d_name:
                    self.goal += 1
                    # init
                    self.SmellSpot[self.i_name.index(self.d_name)][1] = "none"

            else:
                print("<< You can get enough data, Good job. >>") #VIS
                """
                 it need to avoid with  division by zero
                """
                self.Agent[i][1] += math.inf
                break

    def move(self, next_p, i):
        self.Agent[i][1] += self.check_weight(self.Agent[i][0], next_p)
        self.Agent[i][0] = next_p
        # marking
        self.SmellSpot[self.i_name.index(next_p)][1] = str(i)

    def check_weight(self, a, b):
        return self.G.edges[a, b]['weight']

    def check_around(self, now_position):
        neighbors = list(self.G.neighbors(now_position))

        can_reach = []
        for i in neighbors:
            if self.SmellSpot[self.i_name.index(i)][1] == "none":
                can_reach += [self.SmellSpot[self.i_name.index(i)]]

        r_list = []
        weight_list = []
        length = len(can_reach)
        
        for i in range(length):
            #get range(distance)
            r_list += [can_reach[i][2]]
            
            neighbor_position = can_reach[i][0]
            weight_list += [self.check_weight(now_position, neighbor_position)]
            
        """
        consider adjusment of r_list.
        this is the most important part of all set value.
        the agent will decide to move to the next positin by smell_value.
        """
        
        new_smell_value = []
        for i in range(length):
            new_smell_value +=  [r_list[i] / weight_list[i]]


        if len(r_list) == 0:
            print("( I couldn't reach, Let me stop. )") #VIS
            return "stop"
        else:
            return can_reach[r_list.index(max(r_list))][0]
            # return can_reach[new_smell_value.index(max(new_smell_value))][0]
        
        
    def result(self):
        
        # for i in range(self.Agent.count([self.s_name ,0])):
        #     self.Agent.remove([self.s_name ,0])
            # self.Agent.remove([0,0])
        
        aggregated  = [row[1] for row in self.Agent]
        score = min(aggregated)
        print(aggregated)
        
        if score == math.inf:
            self.plot()
            
        # """
        print("\n################################")
        print("Best of SDA Answer")
        print(" length : %f " % score)
        # print("( Agent %d )" % self.Agent.index(min(self.Agent)))
        print("################################")
        # """
        return score
        
