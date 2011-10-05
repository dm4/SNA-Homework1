#!/usr/bin/env python

import matplotlib.pyplot as plt
import math
import matplotlib.text as tt

# our life data
f = open('output/life_time', 'r')
life_x = []
life_data = []
total = 0
for line in f:
    element = line.split()
    life_x.append(int(element[0]))
    life_data.append(int(element[1]))
    total += int(element[1])
life_data_f = map(lambda x: float(x)/total, life_data)
f.close()

# real life data
f = open('real/life.txt', 'r')
real_data = []
for line in f:
    element = line.split()
    real_data.append(float(element[1]))
f.close()

# our age data
f = open('output/age_distribution', 'r')
age_x = [i*5 for i in range(20)]
age_data = []
total = 0
tmp = [0 for i in range(20)]
for line in f:
    element = line.split()
    age_data.append(int(element[1]))
    total += int(element[1])
for i in range(len(age_data)):
    tmp[i/5] += age_data[i]
age_data = tmp
age_data_f = map(lambda x: float(x)/total, age_data)
f.close()

# real age data
f = open('real/age.txt', 'r')
real_age_x = []
real_age_data = []
for line in f:
    element = line.split()
    real_age_data.append(float(element[1]))
    real_age_x.append(element[0])
f.close()

# read average cc data
f = open('output/CC', 'r')
cc_x = []
cc_data = []
for line in f:
    element = line.split()
    cc_x.append(int(element[0]))
    cc_data.append(float(element[1]))
f.close()

# read average sp data
f = open('output/SP', 'r')
sp_x = []
sp_data = []
for line in f:
    element = line.split()
    sp_x.append(int(element[0]))
    sp_data.append(float(element[1]))
f.close()

# read degree data
f = open('output/degree', 'r')
degree_data_all = []
degree_sum = []
i = 0
for line in f:
    element = line.split()
    if (element[0] == 'Cycle'):
        i = int(element[1])
        degree_data_all.append([])
        degree_sum.append(0)
        continue
    degree_data_all[i].append(int(element[1]))
    degree_sum[i] += int(element[1])
f.close()
t = len(degree_data_all) - 1
degree_x = [[], [], [], []]
degree_data = [[], [], [], []]
degree_cycle = (t/2, 3*t/4, 7*t/8, t)
for i in range(4):
    c = degree_cycle[i]
    for j in range(len(degree_data_all[c])):
        d = degree_data_all[c][j]
        degree_x[i].append(j)
        degree_data[i].append(float(d)/float(degree_sum[c]))

# read alpha data for calculate KL-divergence
alpha_data = []
f = open('output/alpha', 'r')
for line in f:
    element = line.split()
    alpha_data.append(float(element[1]))
f.close()

# calculate degree distribution KL-divergence
for i in range(4):
    cycle = degree_cycle[i]
    C = 0
    for k in range(4, len(degree_data_all[cycle])):
        C += pow(k, -alpha_data[cycle])
    C = pow(C, -1)
#    print "cycle %d, alpha %f, C %f" % (cycle, alpha_data[cycle], C)
    D = 0
    adjust_pk = 0
    for k in range(4, len(degree_data_all[cycle])):
        adjust_pk += degree_data[i][k]
    for k in range(4, len(degree_data_all[cycle])):
        pk = degree_data[i][k] / adjust_pk
        qk = C * pow(k, -alpha_data[cycle])
#        print "pk %f, qk %f" % (pk, qk)
        if pk != 0 and qk != 0:
            D += pk * math.log(pk/qk, 2)
            D += qk * math.log(qk/pk, 2)
    print "Cycle %4d, alpha %f, symmetric KL-divergence %f" % (cycle, alpha_data[cycle], D)

# read node edge data
f = open('output/node_edge', 'r')
node_data = []
edge_data = []
for line in f:
    element = line.split()
    node_data.append(int(element[1]))
    edge_data.append(int(element[2]))
f.close()

# read diameter data
f = open('output/diameter', 'r')
diameter_data = []
cycle_data = []
for line in f:
    element = line.split()
    cycle_data.append(int(element[0]))
    diameter_data.append(int(element[1]))
f.close()

# read GC data
f = open('output/GCC', 'r')
GCrate_data = []
iteration_data = []
GCrate_data2 = []
iteration_data2 = []
i=0
for line in f:
    element = line.split()
    iteration_data.append(int(element[0]))
    GCrate_data.append(float(element[1])*100)
    if i%20==0:
        iteration_data2.append(int(element[0]))
        GCrate_data2.append(float(element[1])*100)
    i+=1
f.close()

# draw life.png
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(life_x, life_data_f, 'r-')
bx = fig.add_subplot(111)
bx.plot(life_x, real_data[0:len(life_x)], 'b-')
plt.xlabel('Life Time')
plt.grid(True)
plt.savefig("image/life.png", dpi=200)

# draw age.png
fig = plt.figure()
cx = fig.add_subplot(111)
cx.plot(age_x, age_data_f, 'r-')
cx = fig.add_subplot(111)
cx.plot(age_x, real_age_data[0:len(age_x)], 'b-')
cx.set_xticklabels(['0~4', '20~24', '40~44', '60~64', '80~84'])
cx.set_xticks(range(0, 100, 20))
plt.xlabel('Age')
cx.grid(True)
plt.savefig("image/age.png", dpi=200)

# draw CC.png
fig = plt.figure()
dx = fig.add_subplot(111)
dx.plot(cc_x, cc_data, 'r-', picker=5)
plt.ylabel('clustering coefficient')
plt.grid(True)
plt.savefig("image/CC.png", dpi=200)

# draw SP.png
fig = plt.figure()
ex = fig.add_subplot(111)
ex.plot(sp_x, sp_data, 'r-', picker=5)
plt.ylabel('shortest path')
plt.grid(True)
plt.savefig("image/SP.png", dpi=200)

# draw degree.png
fig = plt.figure()
for i in range(4):
    ex = fig.add_subplot(221 + i)
    ex.loglog(degree_x[i], degree_data[i], 'r-')
    plt.subplots_adjust(hspace=0.5, wspace=0.4)
    plt.title('Cycle ' + str(degree_cycle[i]))
    plt.xlabel('degree k')
    plt.ylabel('P(k)')
    plt.grid(True)
plt.savefig("image/degree.png", dpi=200)

# draw node_edge.png
fig = plt.figure()
x = fig.add_subplot(111)
x.loglog(node_data, edge_data, 'r-')
plt.grid(True)
plt.xlabel('Number of nodes')
plt.ylabel('Number of edges')
plt.savefig('image/node_edge.png', dpi=200)

# draw GC.png
fig = plt.figure()
GC = fig.add_subplot(111)
GC.plot(iteration_data, GCrate_data, 'r-', linewidth=2)
GC.plot(iteration_data2, GCrate_data2, 'ks')

plt.xlabel("iterations (cycles)")
plt.ylabel("relative size of the GC")
GC.set_yticklabels(['92%', '94%', '96%', '98%', '100'])
GC.set_yticks(range(92, 100, 2))
GC.grid(True)
plt.savefig("image/GC.png", dpi=200)

# draw diameter.png
fig = plt.figure()
dx = fig.add_subplot(111)
dx.plot(cycle_data, diameter_data, 'r-', picker=5)
plt.xlabel("Cycle")
plt.ylabel("Diameter")
dx.grid(True)
plt.savefig("image/diameter.png", dpi=200)
