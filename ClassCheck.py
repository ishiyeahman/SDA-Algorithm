import networkx as nx
from networkx.drawing.nx_pylab import apply_alpha
# import Smell_Detection_Agent_Algorithm as sda
# import SDAsequential as sda
# import SDAparallel as sda
# import SDAparallel_beta as sda
# import SDAparallel_beta as sda
import SDAsequential_overRide as sda
# import SDAparallel_overRide as sda
import numpy as np



def main():
    make_graph()


def make_graph():
    G = nx.Graph()
    # color_map = [ 'lightblue' for i in range(len(G) )]    
    
    label = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n","o"]
    
    """
    pos = {label[0]: (0, 2),
           label[1]: (2, 4),
           label[2]: (4, 3.5),
           label[3]: (3, 0.5),
           label[4]: (6, 1.5),
           label[5]: (5, 5.5),
           label[6]: (7, 3),
           label[7]: (8, 5),
           #---
           label[8]: (3, 3),
           label[9]: (5, 9),
           label[10]: (8, 9),
           label[11]: (1, 8),
           label[12]: (8, 8),
           label[13]: (7, 8),
           label[14]: (4, 10),
           }
    """
    pos = {label[0]: [0, 2],
           label[1]: [2, 4],
           label[2]: [4, 3.5],
           label[3]: [3, 0.5],
           label[4]: [6, 1.5],
           label[5]: [5, 5.5],
           label[6]: [7, 3],
           label[7]: [8, 5],
           #---
           label[8]: [3, 3],
           label[9]: [5, 9],
           label[10]: [8, 9],
           label[11]: [1, 8],
           label[12]: [8, 8],
           label[13]: [7, 8],
           label[14]: [4, 10],
           }
    
    print(pos)
    
    G.add_edge("a", "b", weight=10)
    # G.add_edge("a", "c", weight=16)
    G.add_edge("a", "d", weight=15)
    G.add_edge("b", "c", weight=18)
    G.add_edge("b", "e", weight=17)
    G.add_edge("c", "d", weight=13)
    G.add_edge("c", "e", weight=11)
    G.add_edge("c", "f", weight=10)
    G.add_edge("c", "g", weight=19)
    G.add_edge("d", "e", weight=15)
    G.add_edge("d", "g", weight=18)
    G.add_edge("f", "h", weight=13)
    G.add_edge("g", "h", weight=18)
    G.add_edge("i", "a", weight=14)
    G.add_edge("i", "b", weight=16)
    G.add_edge("i", "d", weight=18)
    G.add_edge("i", "h", weight=17)
    G.add_edge("j", "c", weight=14)
    G.add_edge("j", "h", weight=18)
    # G.add_edge("k", "a", weight=10)
    G.add_edge("k", "f", weight=18)
    G.add_edge("k", "g", weight=13)
    G.add_edge("k", "e", weight=17)
    G.add_edge("k", "j", weight=17)
    G.add_edge("l", "a", weight=18)
    G.add_edge("l", "c", weight=16)
    G.add_edge("l", "f", weight=11)
    G.add_edge("l", "g", weight=12)
    G.add_edge("l", "j", weight=15)
    G.add_edge("h", "m", weight=10)
    G.add_edge("j", "n", weight=12)
    G.add_edge("o", "l", weight=11)
    G.add_edge("o", "j", weight=16)
    G.add_edge("o", "b", weight=19)
    G.add_edge("o", "m", weight=13)
    
    # print(G["a"]["k"]["weight"])
    
    
    
    for i in label:
        for j in label:
            if j in G[i]:
                G[i][j]["weight"] = round( weight(i, j, pos), 2)
                
        


    edge_labels = {(i, j): w['weight'] for i, j, w in G.edges(data=True)}
  

    # nx.draw_networkx_edge_labels(G,pos, edge_labels=edge_labels) #VIS
    # nx.draw_networkx(G, pos, with_labels=True, width=0.5)         #VIS
    """
    result = []
    for i in range(10):
        s = sda.Algorithm(G, pos, label[label.index("a")], label[label.index("k")], label)
        s.output()
        s.answer()
        print(s.sortAgent())
        # print(G['a']['x']['weight'])
        # print(s)
        s.plot()
        result += [s.BestScore]
        
        #dijkstra#
        # source = "a"
        # destination = "k"
        # print(nx.dijkstra_path_length(G,source, destination))
        # print(nx.dijkstra_path(G, source , destination))
        # s.plot()
        
    print(min(result))
    print(result)
    """
    
    s = sda.Algorithm(G, pos, label[label.index("a")], label[label.index("k")], label)
    print(s.BestScore)
    # print(s.ss)
    s.answer()
    
    
    
    
    # print(s.sortAgent())
    s.plot()
    
    
    

def weight(fr, to, pos): 
    
    return np.sqrt((pos[fr][0] - pos[to][0])** 2 + (pos[fr][1] - pos[to][1])** 2 )
    
    

if __name__ == "__main__":
    main()
    
    
