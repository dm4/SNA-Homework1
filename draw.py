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

# draw life.png
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(life_x, life_data_f, 'r-', picker=5)
bx = fig.add_subplot(111)
bx.plot(life_x, real_data[0:len(life_x)], 'b-', picker=5)
plt.xlabel('Age')
plt.grid(True)
plt.savefig("image/life.png", dpi=200)

# draw age.png
fig = plt.figure()
cx = fig.add_subplot(111)
cx.plot(age_x, age_data_f, 'r-', picker=5)
cx = fig.add_subplot(111)
cx.plot(age_x, real_age_data[0:len(age_x)], 'b-', picker=5)
cx.set_xticklabels(['0~4', '20~24', '40~44', '60~64', '80~84'])
cx.set_xticks(range(0, 100, 20))
cx.grid(True)
plt.savefig("image/age.png", dpi=200)

