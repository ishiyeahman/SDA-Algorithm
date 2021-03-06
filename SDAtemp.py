import networkx as nx
import matplotlib.pyplot as plt
import math
import pprint

from networkx.classes import graph

# import Agent as agents
# import SmellSpot as ss
count = 0
AgentNum = 20
# folderName = "test02"
colors = ["red", "blue", "yellow", "green", "pink", "cyan", "SeaGreen"]

# class folderSet:
#     def __init__(self, name):
#         self.folderName = name
        
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
    def __init__(self, G, pos, source, destination, node, folderName):
        """ Graph data"""
        self.G = G
        self.pos = pos
        self.len = len(G)
        self.source = source
        self.destination = destination
        self.node = node
        self.folderName = folderName

        """ Agent data"""
        self.N_sda = AgentNum
        # self.N_sda =  100 
        # number of sda 
        #if you'd like to use full cpu -> ' os.cpu_count()'
        
        self.N_ss = self.len  # number of smell spots
        self.N_limit = 10 # the number of who can each the destination
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
                neighbors = self.getNeighbors(number)
                
                if self.agents[number].current == self.destination:
                    self.arrived += 1
                    
                    break
                
                if len(neighbors ) == 0:
                    self.agents[number].total = math.inf
                    self.lost += 1
                    
                    break
                
                self.setSmelValue(number, neighbors)
                next = self.nextSmellSpot(neighbors)
                self.move(number, next)
                
                #view
                print(colors[number%len(colors)])
                self.nodeColor( colors[number%len(colors)], self.agents[number].route)
                self.makeView()
    

        if  self.agents[number].current != self.destination:
            self.agents[number].total = math.inf

        self.ValueDown(self.agents[number].route)
    
        return  self.agents[number].current
    

    def getNeighbors(self, num):
        indexList = []
        neighbors = list(self.G.neighbors(self.agents[num].current))
        for nb in neighbors: 
            for i in range(len(self.ss)):
                if  self.ss[i].nodeName == nb and self.ss[i].nodeName != self.source:
                    # expectTotal = self.agents[num].total + self.G[ self.agents[num].current][self.ss[i].nodeName ]['weight']
                    if (self.ss[i].visitor != self.agents[num].name): #????????????????????????????????????
                        indexList.append(i)

        return indexList
    
    
    def nextSmellSpot(self, nbs):
        max = 0
        maxIndex = 0
        
        for i in nbs:
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
               
                self.ss[i].smellvalue = ( 1 / (self.a + self.b * p) )# /  (self.G[ self.agents[num].current][self.ss[i].nodeName ]['weight'])
                if self.ss[i].nodeName == self.source:
                    self.ss[i].smellvalue = 0 
                
                
    
    def move(self, num, next):
        
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
            
        for i in range(self.N_sda):
            self.action(i)
            
        # """
        

        self.BestAgent = min(self.agents, key=lambda x: x.total)
        self.BestScore =  self.BestAgent.total
        
        
        self.sorted = self.sortAgent()

    
        
        if self.BestScore==0:
            print(self.agents)
            
        
            
        
        
        sorted = self.sortAgent()

        
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
        decrease = 0.1
        
        for node in route:
             for i in range(len(self.ss)):
                
                if self.ss[i].nodeName == node and self.ss[i].nodeName != self.destination and self.ss[i].nodeName != self.source :
                    self.ss[i].smellvalue = self.ss[i].smellvalue*(1-decrease)

    def makeView(self):
        global count
        nx.draw(self.G, self.pos, node_color=self.color_map, with_labels=True)
        plt.savefig('/Volumes/GoogleDrive/??????????????????/HI5/????????????/imgAnime/'+ self.folderName+'/'+str(count)+'.png')
        count += 1
        