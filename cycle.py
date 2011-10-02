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

def computerAlpha(degree):
    xmin = 4
    n = len(degree) + 1
    degree_f = []
    totalDegree = reduce(lambda x, y: x + y, degree)
    for d in degree:
        degree_f.append(float(d)/float(totalDegree))
    s = 0
    for i in range(1, n):
        s += math.log(float(i)/float(xmin))
    s = math.pow(s, -1)
    alpha = 1 + s * n
#    print "alpha: %f" % alpha
    return alpha

quick_mode = False

G = nx.complete_graph(5)
for node in G.nodes():
    G.node[node]['age'] = 0

cycle = 0
nodeNum = 5
maxAge = 0
deathNum = [0 for i in range(3000)]
birthNum = [0 for i in range(3000)]
totalNum = [0 for i in range(3000)]
edgeNum = [0 for i in range(3000)]
deathAge = [0 for i in range(3000)]
spAry = [0 for i in range(3000)]
ccAry = [0 for i in range(3000)]
degreeAry = [0 for i in range(3000)]
diameterAry = [0 for i in range(3000)]
alphaAry = [0 for i in range(3000)]
gccAry = [0 for i in range(3000)]

while len(G.nodes()) < 2000:

    # new nodes
    birthNum[cycle] = len(G.nodes()) / 60
    if birthNum[cycle] < 100:
        birthNum[cycle] = 100
    for i in range(birthNum[cycle]):
        G.add_node(nodeNum, age=0)
        if (not quick_mode):
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

    if (quick_mode):
        print "Cycle %d, node %d" % (cycle, len(G.nodes()))
    else:
        degreeAry[cycle] = nx.degree_histogram(G)
        alpha = computerAlpha(degreeAry[cycle])
        giant_connected_component = nx.connected_component_subgraphs(G)[0]
        sp = nx.average_shortest_path_length(giant_connected_component)
        cc = nx.average_clustering(G)
        diameter = nx.algorithms.distance_measures.diameter(giant_connected_component)
        gcc = float(len(giant_connected_component))/len(G.nodes())
        nodes = len(G.nodes())
        edges= len(G.edges())
        print "Cycle %d,\tnode %d,\tedge %d,\tsp %f,\tcc %f,\tdiameter %d,\talpha %f, gcc %f" % (cycle, nodes, edges, sp, cc, diameter, alpha, gcc)
        spAry[cycle] = sp
        ccAry[cycle] = cc
        diameterAry[cycle] = diameter
        alphaAry[cycle] = alpha
        gccAry[cycle] = gcc
        totalNum[cycle] = nodes
        edgeNum[cycle] = edges

    cycle += 1

# log
fsp = open('output/SP', 'w')
fcc = open('output/CC', 'w')
fdegree  = open('output/degree', 'w')
fd = open('output/diameter', 'w')
falpha = open('output/alpha', 'w')
fgcc = open('output/GCC', 'w')
fbd = open('output/birth_death', 'w')
for i in range(cycle):
    fsp.write('%d\t%f\n' % (i, spAry[i]))
    fcc.write('%d\t%f\n'% (i, ccAry[i]))
    fdegree.write('Cycle%d\n' % i)
    for k in range(len(degreeAry[i])):
        fdegree.write('%d\t%d\n' % (k, degreeAry[i][k]))
    fd.write('%d\t%d\n' % (i, diameterAry[i]))
    falpha.write('%d\t%f\n' % (i, alphaAry[i]))
    fgcc.write('%d\t%f\n' % (i, gccAry[i]))
    fbd.write('%d\t%d\t%d\t%f\n' % (i, birthNum[i], deathNum[i], float(deathNum[i])/float(birthNum[i])))
fd.close()
fsp.close()
fcc.close()
fdegree.close()
falpha.close()
fgcc.close()
fbd.close()

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
