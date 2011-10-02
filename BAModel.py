import networkx as nx
import random

def addnode(G, newnode,  m):
    
    problist = []

    for node in G.nodes():
        for i in range(nx.degree(G, node)):
            problist.append(node)
    
    connectlist = []
    n = m
    while (n>0):
        r = random.randrange(0, len(problist))
        if (isNodeInList(connectlist, problist[r])==False):
            connectlist.append(problist[r])
            G.add_edge(newnode, problist[r])
            n=n-1
            
    #print connectlist
    return G
    
    
def isNodeInList(alist, node):
    for n in alist:
        if (node == n):
            return True
    return False

#import matplotlib.pyplot as plt

#graph = nx.complete_graph(5)

#for k in range(5, 3000):
#    graph = addnode(graph, k, 4)

#print nx.nodes(graph)

#print nx.average_clustering(graph)
#print nx.average_shortest_path_length(graph)

#print(graph.edges())
#nx.draw_networkx(graph)
#plt.savefig("g.png")


