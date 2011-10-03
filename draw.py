#!/usr/bin/env python

import matplotlib.pyplot as plt

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
plt.subplots_adjust(wspace=20.0)
fig = plt.figure()
for i in range(4):
    ex = fig.add_subplot(221 + i)
    ex.loglog(degree_x[i], degree_data[i], 'r-')
    plt.subplots_adjust(hspace=0.5, wspace=0.4)
    plt.title('Cycle ' + str(degree_cycle[i]))
    plt.grid(True)
plt.savefig("image/degree.png", dpi=200)
