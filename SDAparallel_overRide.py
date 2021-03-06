import networkx as nx
import matplotlib.pyplot as plt
import math
from concurrent.futures import ThreadPoolExecutor
# from concurrent.futures import ProcessPoolExecutor
from concurrent import futures
import pprint
import time
import random
from networkx.classes import graph

# import Agent as agents
# import SmellSpot as ss

class Agent:
    def __init__(self, name, total, current):
        self.name = name
        self.total = total
        self.current = current
        #adding
        self.route = [current]
        
    def __repr__(self):
        return self.__class__.__name__ + pprint.pformat(self.__dict__)  
        
class SmellSpot:
    def __init__(self, nodeName, visitor, smellvalue):
        self.nodeName = nodeName
        self.visitor = visitor
        self.smellvalue = smellvalue
        self.visitorTotal = math.inf
        
    def __repr__(self):
        return self.__class__.__name__ + pprint.pformat(self.__dict__)  
        
class Algorithm:
    def __init__(self, G, pos, source, destination, node):
        """ Graph data"""
        self.G = G
        self.pos = pos
        self.len = len(G)
        self.source = source
        self.destination = destination
        self.node = node

        """ Agent data"""
        self.N_sda =  100 # number of sda 
        #if you'd like to use full cpu -> ' os.cpu_count()'
        
        self.N_ss = self.len  # number of smell spots
        self.N_limit = 100 # the number of who can each the destination
        self.a = 10  # init smell values
        self.b = 1 # Decrease Constant
        # self.r = self.distance()
        
        self.arrived = 0
        self.lost = 0 #the number is the agents that be lost
        self.adjacent = list(self.G.neighbors(self.destination))
        
        # agents setting
        self.agents = []
        for i in range(self.N_sda):
            self.agents.append(Agent(i , 0, self.source) )

        # smellspots setting
        self.ss = []
        for i in range(self.N_ss):
            self.ss.append(SmellSpot(self.node[i] , 'none', 'unknown') )
            if self.node[i] == self.source:
                 self.ss[i].visitor = 'init'
                 self.ss[i].smellvalue = -math.inf
            if self.node[i] == self.destination :
                 self.ss[i].visitor = 'Agent in goal >> '
                
                
        self.color_map = [ 'lightblue' for i in range(self.len )]    
        self.main()
        
        
        
    """    
    def distance(self, _from, to):
        return math.dist(self.pos[_from], self.pos[to])
    """
    
    def distance(self, _from):
        return math.dist(self.pos[_from], self.pos[self.destination])
    
    
    def action(self, number):
        
        if self.lost == self.N_sda:
            print("- We can't arrive ...")
            self.agents[number].total = math.inf
            self.plot()
        elif self.arrived >= self.N_limit:
                self.agents[number].total = math.inf
        else:
            while(self.arrived < self.N_limit ):
                
                # time.sleep(random.random()/1000)
                # print('go')
                neighbors = self.getNeighbors(number)
                
                if self.agents[number].current == self.destination:
                    self.arrived += 1
                    # pprint.pprint(self.agents[number])
                    # print("- I am just arrived destination now")
                    # self.leave(self.agents[number].route)
                    break
                
                if len(neighbors ) == 0:
                    # pprint.pprint(self.agents[number])
                    print("- I can't arrive ...")
                    self.agents[number].total = math.inf
                    """
                    myloot = self.agents[number].route
                    myloot.pop()
                    self.leave(myloot)
                    """
                    # self.deadEnd(myloot)
                    # self.plot()

                    self.lost += 1
                    # self.N_sda += 1
                    break
                
                self.setSmelValue(number, neighbors)
                next = self.nextSmellSpot(neighbors)
                self.move(number, next)
                
                
                
        if  self.agents[number].current != self.destination:
            self.agents[number].total = math.inf
        
        
        self.ValueDown(self.agents[number].route)
    
        return  self.agents[number].current
    
    def leave(self, nodes):
        
        #messy
        for node in nodes:
            for i in range(len(self.ss)):
                if self.ss[i].nodeName == node:
                    self.ss[i].visitor = 'none'
                    self.ss[i].visitorTotal = math.inf
                    # print('delete')
                       
                    
                    
    def deadEnd(self, nodes):
        nodes = reversed(nodes)
        keep = True
        for node in nodes:
            for i in range(len(self.ss)):
                if self.ss[i].nodeName == node:
                    if keep and len(list(self.G.neighbors(node))) < 2:
                        self.ss[i].visitor = 'dead'
                        self.ss[i].smellvalue = 0
                        print('delete')
                    else:
                        keep = False

    def getNeighbors(self, num):
        indexList = []
        neighbors = list(self.G.neighbors(self.agents[num].current))
        for nb in neighbors: 
            for i in range(len(self.ss)):
                if  self.ss[i].nodeName == nb and self.ss[i].nodeName != self.source:
                    # expectTotal = self.agents[num].total + self.G[ self.agents[num].current][self.ss[i].nodeName ]['weight']
                    if (self.ss[i].visitor != self.agents[num].name): #????????????????????????????????????
                        indexList.append(i)
                    
                    """
                    if (self.ss[i].visitor == 'none') or (self.ss[i].nodeName == self.destination) or (expectTotal <= self.ss[i].visitorTotal):
                        indexList.append(i)
                        
                        # if((expectTotal < self.ss[i].visitorTotal)):
                            # time.sleep(random.random()/1000)
                        #     # time.sleep(0.0001)
                            # print("expect!!")
                            # print(self.agents[num])
                        # # permit overRide
                    """
        return indexList
    
    
    def nextSmellSpot(self, nbs):
        max = 0
        maxIndex = 0
        
        # nbs.remove(self.source)
        for i in nbs:
            # if self.ss[i].visitor != 'none':
            #     maxIndex = i
            if self.ss[i].nodeName == self.destination:
                maxIndex = i
                break
            elif max < self.ss[i].smellvalue:
                max = self.ss[i].smellvalue
                maxIndex = i
        return maxIndex 
    
    
    def setSmelValue(self, num, nbs):
        for i in nbs:
            if self.ss[i].visitor == 'none':
                p = self.distance(self.ss[i].nodeName)
                # self.ss[i].smellvalue =  1 / (self.a + self.b * p)       
                self.ss[i].smellvalue = ( 1 / (self.a + self.b * p) )# /  (self.G[ self.agents[num].current][self.ss[i].nodeName ]['weight'])
                # self.ss[i].smellvalue =  ( 1 / (self.a + self.b * p) ) - self.G[ self.agents[num].current][self.ss[i].nodeName ]['weight']
                # if self.ss[i].nodeName in self.adjacent:
                #     self.ss[i].smellvalue = self.a - 1 / (self.G[self.destination][self.ss[i].nodeName ]['weight'] + self.G[ self.agents[num].current][self.ss[i].nodeName ]['weight'])
                    
                # if self.ss[i].nodeName == self.destination:
                #     self.ss[i].smellvalue = self.a
                if self.ss[i].nodeName == self.source:
                    self.ss[i].smellvalue = 0 
                
                
    
    def move(self, num, next):
        #new struct
        self.ss[next].visitorTotal = self.agents[num].total
        
        self.agents[num].total += self.G[ self.agents[num].current][self.ss[next].nodeName ]['weight']
        self.agents[num].route.append(self.ss[next].nodeName)
    
        self.agents[num].current = self.ss[next].nodeName
        if self.ss[next].nodeName == self.destination:
            self.ss[next].visitor += (str(self.agents[num].name) + ' ')
        else:
            self.ss[next].visitor = self.agents[num].name

            
    def main(self):
        max_workers = self.N_sda
        futureList = []
    
        # """
        # when max_workers = None, it means max_workers = 5*os.cpu_count()
        with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="thread") as executor:
        # In using 'ProcessPoolExecutor' case, each process would be proceeded by order. ===> BUT, this method can't share a memory so it would be cause of bug.
        # with ProcessPoolExecutor(max_workers=max_workers) as executor:
            for i in range(self.N_sda):
                future = executor.submit(self.action, i)
                futureList.append(future)
                if future == self.destination:
                    print('Goal')
                
            # print([x.result() for x in futureList])
        """    
            
        for i in range(self.N_sda):
            self.action(i)
            
        # """
        

        self.BestAgent = min(self.agents, key=lambda x: x.total)
        self.BestScore =  self.BestAgent.total
        
        # print(self.BestAgent)
        self.sorted = self.sortAgent()
        # print(sorted[0])
        # print(sorted[1])
        # print(sorted[2])
    
        
        if self.BestScore==0:
            print(self.agents)
            
        
            
        
        
        sorted = self.sortAgent()
        """
        self.nodeColor('red', sorted[0].route)
        self.nodeColor('pink', sorted[1].route)
        self.nodeColor('gray', sorted[2].route)
        self.nodeColor('green', [self.destination])
        self.nodeColor('blue', [self.source])
        """
        
        # if self.BestScore == math.inf:
        #     self.plot()
        
    def plot(self):
        nx.draw(self.G, self.pos, node_color=self.color_map, with_labels=True)
        plt.show()
        
    def answer(self):
        print("SDA-Algorithm Best Path >> ")
        self.output(self.BestAgent)
        
    def output(self, target ):
        print(target.name)
        print(target.total)
        print(target.route)
        
    def sortAgent(self):
        return sorted(self.agents, key=lambda x: x.total)
    
    def nodeColor(self, color, nodes):
        graph = list(self.G.nodes())
        for n in self.G:
            if n in nodes:
                self.color_map[graph.index(n)] = color
                
    def ValueDown(self, route):
        decrease = 0.2
        
        for node in route:
             for i in range(len(self.ss)):
                
                if self.ss[i].nodeName == node and self.ss[i].nodeName != self.destination and self.ss[i].nodeName != self.source :
                    self.ss[i].smellvalue = self.ss[i].smellvalue*(1-decrease)
                 
                
                    
                    
            
        
        
                              
    # def overRide(self):