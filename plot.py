#!/usr/bin/python3

import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt('out.txt', skiprows=1, comments='Error(', dtype='S21')

stats_dtype = [('name', 'S21'), ('median', float)]
stats = np.array([], dtype=stats_dtype)

while data.size > 0:
    sub_name = data[0,0]
    mask = data[:,0] == sub_name
    scores = data[mask,1]
    data = data[~mask]

    scores = scores.astype('f')
    #stats.append( (sub_name, np.median(scores), np.percentile(scores, 25), np.percentile(scores, 75)) )
    stats = np.append(stats, np.array([(sub_name, np.median(scores))], dtype=stats_dtype))

stats = np.sort(stats, order='median')

fix, ax = plt.subplots()

x_pos = np.arange(len(stats))
ax.bar(x_pos, stats['median'])
ax.set_xticks(x_pos)
names = stats['name']
names = map(lambda n: n.decode('utf-8'), names)
ax.set_xticklabels(names)
ax.set_ylabel('Grade Level')
ax.set_title('Median Reddit Comment Grade Level')

plt.setp(ax.xaxis.get_majorticklabels(), rotation=70, horizontalalignment='right')

plt.show()
