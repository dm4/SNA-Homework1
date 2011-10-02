#!/usr/bin/env python
import networkx as nx
import random
import BAModel
import math

def deathRate(age):
    rate = -2.0/(age-100.1) - 0.02
    if age == 0:
        rate += 0.001
    elif age < 60:
        rate = rate / (1 + ((60 -age) / 60.0) * 10)
    return rate

G = nx.complete_graph(5)
for node in G.nodes():
    G.node[node]['age'] = 0

cycle = 0
nodeNum = 5
maxAge = 0
deathNum = [0 for i in range(3000)]
birthNum = [0 for i in range(3000)]
totalNum = [0 for i in range(3000)]
deathAge = [0 for i in range(3000)]
spAry = [0 for i in range(3000)]
ccAry = [0 for i in range(3000)]

while len(G.nodes()) < 10000:
    totalNum[cycle] = len(G.nodes())

    # new nodes
    birthNum[cycle] = len(G.nodes()) / 50
    if birthNum[cycle] < 100:
        birthNum[cycle] = 100
    for i in range(birthNum[cycle]):
        G.add_node(nodeNum, age=0)
        BAModel.addnode(G, nodeNum, 4)
        nodeNum += 1

    # check if node is dead
    for node in G.nodes():
        prob = deathRate(G.node[node]['age'])
        r = random.random()
        if r > prob:
            G.node[node]['age'] += 1
        else:
            if G.node[node]['age'] > maxAge:
                maxAge = G.node[node]['age']
            deathNum[cycle] += 1
            deathAge[G.node[node]['age']] += 1
            G.remove_node(node)

    sp = nx.average_shortest_path_length(nx.connected_component_subgraphs(G)[0])
    cc = nx.average_clustering(G)
    print "Cycle %d, node %d, sp %f, cc %f" % (cycle, len(G.nodes()), sp, cc)
    spAry[cycle] = sp
    ccAry[cycle] = cc

    cycle += 1
    

#print "Cycle\tbirth\tdeath\ttotal\tdeath rate"
#for i in range(cycle):
#    print "%d\t%d\t%d\t%d\t%f" % (i, birthNum[i], deathNum[i], totalNum[i], float(deathNum[i])/totalNum[i])

fsp = open('output/SP', 'w')
fcc = open('output/CC', 'w')
for i in range(cycle):
    fsp.write('%d\t%f\n' % (i, spAry[i]))
    fcc.write('%d\t%f\n'% (i, ccAry[i]))
fsp.close()
fcc.close()

#print "Life Distribution"
f = open('output/life_time', 'w')
for i in range(maxAge + 1):
#    print "%d\t%d" % (i, deathAge[i])
    f.write("%d\t%d\n" % (i, deathAge[i]))
f.close()

#print "Age Distribution"
f = open('output/age_distribution', 'w')
finalMaxAge = 0
finalAgeNum = [0 for i in range(200)]
for node in G.nodes():
    age = G.node[node]['age']
    if age > finalMaxAge:
        finalMaxAge = age
    finalAgeNum[age] += 1
for i in range(finalMaxAge + 1):
#    print "%d\t%d" % (i, finalAgeNum[i])
    f.write("%d\t%d\n" % (i, finalAgeNum[i]))
